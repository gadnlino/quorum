from flask import Flask
from flask_restx import Api, Resource, fields

from constants.constants import DB_LOCATION
from repository.repository import Repository

## creating Flask app and api

app = Flask(__name__)
api = Api(app, version='1.0.0', doc='/docs', title='Reports API', description='Legislator and Bills - Reports API')

## defining return models

legislator_activity_model = api.model('LegislatorActivity', {
    'Legislator ID': fields.Integer(description='The unique identifier of the legislator.'),
    'Legislator': fields.String(description='The name of the legislator.'),
    'Supported bills': fields.Integer(description='The number of bills the legislator voted in favor of.'),
    'Opposed bills': fields.Integer(description='The number of bills the legislator voted against.'),
})

bill_voting_result_model = api.model('BillVotingResult', {
    'Bill ID': fields.Integer(description='The unique identifier of the bill.'),
    'Bill': fields.String(description='The title of the bill.'),
    'Supporters': fields.Integer(description='The number of legislators that voted in favor of the bill.'),
    'Opposers': fields.Integer(description='The number of legislators that voted against the bill..'),
    'Primary sponsor': fields.String(description='The legislator that proposed the bill.'),
})

## defining api routes

reports_namespace = api.namespace('reports')

@reports_namespace.route('/legislator-activity')
class LegislatorActivityReport(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.__repository = Repository(DB_LOCATION)
        
        super().__init__(api, *args, **kwargs)

    @reports_namespace.marshal_list_with(legislator_activity_model)
    def get(self,):
        """Returns the number of approved and opposed bills for each legislator."""
        return self.__repository.get_legislator_activity(), 200
    
@reports_namespace.route('/bill-voting-results')
class LegislatorActivityReport(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.__repository = Repository(DB_LOCATION)
        
        super().__init__(api, *args, **kwargs)
    
    @reports_namespace.marshal_list_with(bill_voting_result_model)
    def get(self,):
        """Returns the approvals and rejections for each bill."""
        return self.__repository.get_bill_voting_results(), 200

if __name__ == '__main__':
    app.run()