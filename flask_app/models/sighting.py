from asyncio.windows_events import NULL
from flask_app.models import login
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

class Sighting:
    database ="sasquatch_schema"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_sighting = data['date_sighting'] #datetime
        self.num_of_sas = data['num_of_sas'] #int
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.login_id = data['login_id']
        self.reported_by = None
        self.skeptics = []
    
    #if i had made a super class about sighting but accepting a skeptics count from mysql
    # class Sighting_with_Skeptic_Count(Sighting):
    #     def __in__(self, data):
    #         super(data)


    @classmethod 
    def insert_sas(cls,data):
        query = "INSERT INTO sightings (location , what_happened , date_sighting , num_of_sas , login_id) VALUES (%(location)s , %(what_happened)s , %(date_sighting)s , %(num_of_sas)s, %(login_id)s ) ;"
        return connectToMySQL(cls.database).query_db(query,data)

    @staticmethod
    def validate_report(data):
        is_valid = True 
        if len(data['location']) < 1:
            flash('All feilds must be filled out', 'report')
            is_valid = False 
        if len(data['what_happened']) < 1:
            flash('All feilds must be filled out', 'report')
            is_valid = False 
        if len(data['date_sighting']) == NULL :
            flash('All feilds must be filled out', 'report')
            is_valid = False 
        if len(data['num_of_sas'])< 1:
            flash('Number of Sasquatches must be at least 1', 'report')
            is_valid = False 
        return is_valid

    @classmethod
    def update_sas(cls,data):
        query = "UPDATE sightings SET location = %(location)s, what_happened = %(what_happened)s, date_sighting = %(date_sighting)s , num_of_sas = %(num_of_sas)s   WHERE id = %(id)s "
        return connectToMySQL(cls.database).query_db(query,data)


    @classmethod 
    def get_all_sas(cls):
        query = "SELECT * FROM sightings JOIN logins on sightings.login_id = logins.id ;"
        results = connectToMySQL(cls.database).query_db(query)
        return results

    @classmethod 
    def get_by_sas_id(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s ;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return cls(results[0])
    
    @classmethod 
    def get_by_sas_id_plus_login(cls,data):
        query = "SELECT * FROM sightings JOIN logins on sightings.login_id = logins.id WHERE sightings.id = %(id)s ;"
        result = connectToMySQL(cls.database).query_db(query,data)
        instance = cls(result[0])
        for row in result:
            login_data ={
                'id':row['logins.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['logins.created_at'],
                'updated_at':row['logins.updated_at']
            }
            instance.reported_by =login.Login(login_data)
        return instance


    @classmethod
    def add_skeptic(cls,data):
        query= "INSERT INTO skeptics (login_id, sighting_id) VALUE (%(login_id)s , %(sighting_id)s ); "
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def show_skeptics(cls,data):
        query = "SELECT * from skeptics JOIN logins on skeptics.login_id = logins.id WHERE skeptics.sighting_id = %(id)s ;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return results



    @classmethod 
    def all_skeptics(cls):
        query= 'SELECT * FROM skeptics;'
        return connectToMySQL(cls.database).query_db(query)

    @classmethod
    def delete_skeptic(cls,data):
        query = "DELETE FROM skeptics WHERE login_id = %(login_id)s and sighting_id = %(sighting_id)s ; "
        return connectToMySQL(cls.database).query_db(query,data)

    
    @classmethod
    def delete_sas(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)
    








    #if i had gon the route of making a count funtion on python instead of mysql
    @classmethod
    def get_all_sightings_with_skeptics(cls,data):
        query = """
            SELECT * 
            FROM sightings 
            LEFT JOIN skeptics
            """
        results = connectToMySQL(cls.database).query_db(query,data)
        # keep track of sightings already handled while processing results
        sightings_processed =  {1: [], 3: [13], 5: [13,14]} 
        
        # final list of sightings with skeptics
        sightings = []
        for row in results:
            # check for duplicate
            if row.id not in sightings_processed:
                sightings_processed[row.id] = [row.skeptic_id]
                sightings.append(cls(row))
            else:
                sightings_processed[row.id].append(row.skeptic_id)
        
        for sighting in sightings:
            sighting.skeptics = sightings_processed[sighting.id]

        return sightings