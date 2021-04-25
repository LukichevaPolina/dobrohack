# Для Полины и Алены
import sqlite3
import datetime

db = sqlite3.coonect(r'')
cur = db.cursor()

class Database:
    def __init__(self):
        self.users = []

    def create_it_person(self, id, surname, name):
        cur.execute(""" INSERT INTO “ПРЕДСТАВИТЕЛЬ IT” VALUES (id, surname, name, 0);""")

    def create_nko_person(self, ):
        cur.execute(""" INSERT INTO “ПРЕДСТАВИТЕЛЬ НКО” VALUES (id, surname, name);""")

    def create_moderator(self, ):
        cur.execute("""INSERT INTO “МОДЕРАТОР” VALUES (id, surname, name);""")

    def get_spheres(self):
        """ выдает список сфер обязательно всегда в одном и том же порядке (сортируйте по id)"""
        # return ["Дизайн", "Создатель сайтов", "Аналитик", "Дата сайнтист"]
        cur.execute("""SELECT "НАЗВАНИЕ" FROM """)
        pass

    def get_user_spheres(self, username):
        """"""
        # return ["Дизайн", "Создатель сайтов"]
        pass

    def add_spheres2user(self, username, list_id_spheres):
        pass


bot_db = Database()