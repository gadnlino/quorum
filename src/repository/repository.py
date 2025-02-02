import sqlite3

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