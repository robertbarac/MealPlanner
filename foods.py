import sqlite3
from sqlite3.dbapi2 import Cursor, connect

class Food:

    def get_connection(self):
        connection = sqlite3.connect('meal-planner.db')
        connection.text_factory = lambda b: b.decode(errors = 'ignore')
        return connection
        

    def read_foods(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        sql_sentence = "SELECT * FROM food"
        cursor.execute(sql_sentence)
        return cursor.fetchall()

    def add_food(self, food_data):
        connection = self.get_connection()
        cursor = connection.cursor()
        sql_sentence = "INSERT INTO food(food_name, prot_grams, carb_grams, fat_grams) VALUES(?, ?, ?, ?)"
        cursor.execute(sql_sentence, food_data)
        connection.commit()
        connection.close()
    
    def modify_food(self, food_data):
        connection = self.get_connection()
        cursor = connection.cursor()
        sql_sentence = "UPDATE food SET food_name = ?, prot_grams = ?, carb_grams = ?, fat_grams = ? WHERE id = ?"
        cursor.execute(sql_sentence, food_data)
        connection.commit()
        connection.close()
    
    def delete_food(self, food_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        sql_sentence = "DELETE FROM food WHERE id = (?)"
        cursor.execute(sql_sentence, [food_id])
        connection.commit()
        connection.close()
    
    def read_food(self):
        pass
