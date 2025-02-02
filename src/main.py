from flask import Flask
from flask_restx import Api, Resource, fields
import sqlite3

DB_LOCATION = './data/database'

class Repository:
    def __init__(self, db_location):
        self.__db_location = db_location
    
    def __query_to_json(self, cursor):
        return [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    
    def get_legislator_activity(self):
        sql = '''
                    select
                    l.id `Legislator ID`,
                        l.name `Legislator`,
                        coalesce(
                        (
                        select
                            count(1)
                        from
                            vote_results vr
                        where
                            vr.legislator_id = l.id
                            and vr.vote_type = 1
                        group by
                            vr.vote_id,
                            vr.legislator_id),
                        0
                        ) `Supported bills`,
                        coalesce(
                        (
                        select
                            count(1)
                        from
                            vote_results vr
                        where
                            vr.legislator_id = l.id
                            and vr.vote_type = 2
                        group by
                            vr.vote_id,
                            vr.legislator_id),
                        0
                        ) `Opposed bills`
                    from
                        legislators l
                        order by l.name;
        '''
        
        db_connection = sqlite3.connect(self.__db_location)
        cursor = db_connection.cursor()
        
        cursor.execute(sql)
        
        result = self.__query_to_json(cursor)
        
        cursor.close()
        db_connection.close()
        
        return result
    
    def get_bill_voting_results(self):
        sql = '''
                    select 
                    b.id 'Bill ID',
                    b.title 'Bill',
                    (
                        select count(1)
                        from vote_results vr
                        join votes v
                        on v.id = vr.vote_id
                        where v.bill_id = b.id
                        and vr.vote_type = 1
                    ) 'Supporters',
                    (
                        select count(1)
                        from vote_results vr
                        join votes v
                        on v.id = vr.vote_id
                        where v.bill_id = b.id
                        and vr.vote_type = 2
                    ) 'Opposers',
                    coalesce(l.name, 'N/A') 'Primary sponsor'
                    from bills b
                    join votes v2
                    on v2.bill_id = b.id
                    left join legislators l
                    on l.id = b.sponsor_id;
        '''
        
        db_connection = sqlite3.connect(self.__db_location)
        cursor = db_connection.cursor()
        
        cursor.execute(sql)
        
        result = self.__query_to_json(cursor)
        
        cursor.close()
        db_connection.close()
        
        return result

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app, version='1.0.0', doc='/docs', title='Reports API', description='Reports API')

    def run(self):
        self.app.run(debug=True)

app = App()

reports_namespace = app.api.namespace('reports', description='Reports operations')

legislator_activity_model = app.api.model('LegislatorActivity', {
    'Legislator ID': fields.Integer(description='The unique identifier of the legislator.'),
    'Legislator': fields.String(description='The name of the legislator.'),
    'Supported bills': fields.Integer(description='The number of bills the legislator voted in favor of.'),
    'Opposed bills': fields.Integer(description='The number of bills the legislator voted against.'),
})

bill_voting_result_model = app.api.model('BillVotingResult', {
    'Bill ID': fields.Integer(description='The unique identifier of the bill.'),
    'Bill': fields.String(description='The title of the bill.'),
    'Supporters': fields.Integer(description='The number of legislators that voted in favor of the bill.'),
    'Opposers': fields.Integer(description='The number of legislators that voted against the bill..'),
    'Primary sponsor': fields.String(description='The legislator that proposed the bill.'),
})

@reports_namespace.route('/legislator-activity')
class LegislatorActivityReport(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.__repository = Repository(DB_LOCATION)
        
        super().__init__(api, *args, **kwargs)

    @reports_namespace.marshal_list_with(legislator_activity_model)
    def get(self,):
        return self.__repository.get_legislator_activity(), 200
    
@reports_namespace.route('/bill-voting-results')
class LegislatorActivityReport(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.__repository = Repository(DB_LOCATION)
        
        super().__init__(api, *args, **kwargs)
    
    @reports_namespace.marshal_list_with(bill_voting_result_model)
    def get(self,):
        return self.__repository.get_bill_voting_results(), 200

if __name__ == '__main__':
    app.run()