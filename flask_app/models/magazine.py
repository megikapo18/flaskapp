from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Magazine:

    db_name='provim'
    def __init__(self,data):
        self.id=data['id'],
        self.title=data['title'],
        self.description=data['description'],
        self.created_at=data['created_at'],
        self.update_at=data['update_at']
    
    @classmethod
    def getAllMagazine(cls):
        query= 'SELECT * FROM magazines LEFT JOIN users ON magazines.user_id= users.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        magazine= []
        for row in results:
            magazine.append(row)
        return magazine
    
    @classmethod
    def get_user_Magazine(cls,data):
        query= 'SELECT * FROM magazines LEFT JOIN users ON magazines.user_id= users.id;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_magazine_by_id(cls, data):
        query= 'SELECT * FROM magazines WHERE magazines.id = %(magazine_id)s;'
        results= connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM magazines WHERE id=%(magazine_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = 'UPDATE magazines SET title=%(title)s, discription =%(discription)s, user_id = %(user_id)s WHERE magazines.id = %(magazine_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def create_magazine(cls,data):
        query = 'INSERT INTO magazines (title, discription, user_id) VALUES ( %(title)s, %(discription)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def add_subcribe(cls, data):
        query= 'INSERT INTO subcribes (magazine_id, user_id) VALUES ( %(magazine_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def remove_subcribes(cls, data):
        query= 'DELETE FROM subcribes WHERE magazine_id=%(magazine_id)s and user_id=%(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroy_magazine(cls, data):
        query= 'DELETE FROM magazines WHERE magazines.id=%(magazine_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def deleteAllsubcribes(cls, data):
        query= 'DELETE FROM subcribes WHERE subcribes.magazine_id = %(magazine_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if len(magazine['title']) < 2:
            flash("Title must be at least 3 characters.", 'title')
            is_valid = False
        if len(magazine['discription']) < 3:
            flash("Magazine description be at least 3 characters.", 'discription')
            is_valid = False
        return is_valid
    
