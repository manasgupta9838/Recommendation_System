import sqlite3 as sql
import datetime


class Database:
    def __init__(self, db_name='db.sqlite3'):
        self.con = sql.connect(db_name)
        print('connected to dbase')

    def close(self):
        self.con.close()
        print('database disconnected')

    def create_user_table(self):
        query = "CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,user TEXT,email TEXT unique ,password TEXT)"
        try:
            self.con.execute(query)
            print('Table created')
        except Exception as e:
            print(f'error->{e}')

    def add_user(self, user, email, password):
        query = f"INSERT into user VALUES(null, '{user}','{email}','{password}')"
        try:
            self.con.execute(query)
            self.con.commit()
            print('success')
        except Exception as e:
            print(f'error->{e}')

    def create_choice_table(self):
        query = "CREATE TABLE choice (id INTEGER PRIMARY KEY AUTOINCREMENT,userid INTEGER,option TEXT,value TEXT, date TEXT)"
        try:
            self.con.execute(query)
            print('Table created')
        except Exception as e:
            print(f'error->{e}')

    def add_option(self, id, option, value):
        query = f"INSERT into choice VALUES(null, {id},'{option}','{value}','{datetime.datetime.now()}')"
        try:
            self.con.execute(query)
            self.con.commit()
            print('success')
        except Exception as e:
            print(query)
            print(f'error->{e}')

    def get_user(self):
        query = "select * from user"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f'error->{e}')
            return None

    def get_choice_user(self, user_id):
        query = f"select * from choice where userid={user_id} ORDER BY date desc LIMIT 5;"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f'error->{e}')
            return None

    def get_brand(self, userid):
        query = f"select * from choice where userid={userid} AND option Like 'brands'"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f'error->{e}')
            return None
