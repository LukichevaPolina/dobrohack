# Для Полины и Алены
import psycopg2

class Database:
    def __init__(self):
        db = psycopg2.connect("database.db")
        self.cur = db.cursor()
        # self.users = []

    def create_it_person(self, id, surname, name):
        self.cur.execute(""" INSERT INTO “ПРЕДСТАВИТЕЛЬ IT” VALUES (id, surname, name, 0); """)

    def create_nko_person(self, ):
        self.cur.execute(""" INSERT INTO “ПРЕДСТАВИТЕЛЬ НКО” VALUES (id, surname, name); """)

    def create_moderator(self, ):
        self.cur.execute(""" INSERT INTO “МОДЕРАТОР” VALUES (id, surname, name); """)

    def get_spheres(self):
        """ выдает список сфер обязательно всегда в одном и том же порядке (сортируйте по id)"""
        # return ["Дизайн", "Создатель сайтов", "Аналитик", "Дата сайнтист"]
        self.cur.execute(""" SELECT "НАЗВАНИЕ" FROM "СФЕРА"; """)

    def get_user_spheres(self, username):
        """"""
        self.cur.execute(""" SELECT * FROM "СФЕРА - IT" WHERE ID=username; """)

    def add_spheres2user(self, username, list_id_spheres):
        for id_sphere in list_id_spheres:
            self.cur.execute(""" INSERT INTO “СФЕРА - IT” VALUES (id_sphere, username); """)



bot_db = Database()