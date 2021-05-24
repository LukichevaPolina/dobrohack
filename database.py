# Для Полины и Алены
import psycopg2
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, create_engine
from sqlalchemy.orm import mapper, relation, sessionmaker

auth = {'user': 'postgres', 'password': 'pshenokek16'}


class It:
    def __init__(self, _id, surname, name):
        self.id = _id
        self.surname = surname
        self.name = name

    def __repr__(self):
        return


class Nko:
    def __init__(self, _id, surname, name):
        self.id = _id
        self.surname = surname
        self.name = name

    def __repr__(self):
        return


class Moderator:
    def __init__(self, _id, surname, name):
        self.id = _id
        self.surname = surname
        self.name = name

    def __repr__(self):
        return


class Task:
    def __init__(self, _id, customer, sector, executor, description, state):
        self.id = _id
        self.customer = customer
        self.sector = sector
        self.executor = executor
        self.description = description
        self.state = state

    def __repr__(self):
        return


class Sector:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    def __repr__(self):
        return


class Sector_It:
    def __init__(self, sector, it):
        self.sector = sector
        self.it = it


class Database:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://{}:{}@localhost/lab2'.format(auth['user'], auth['password'],
                                                                                          echo=True))
        metadata = MetaData()
        self.it_table = Table('It', metadata,
                         Column('ID', String, primary_key=True),
                         Column('Surname', String),
                         Column('Name', String))

        self.nko_table = Table('Nko', metadata,
                          Column('ID', String, primary_key=True),
                          Column('Surname', String),
                          Column('Name', String))

        self.moderator_table = Table('Moderator', metadata,
                                Column('ID', String, primary_key=True),
                                Column('Surname', String),
                                Column('Name', String))

        self.task_table = Table('Tasks', metadata,
                           Column('ID', Integer, primary_key=True),
                           Column('Customer', String),
                           Column('Sector', String),
                           Column('Executor', String),
                           Column('Description', String),
                           Column('State', Integer))

        self.sector_table = Table('Sector', metadata,
                             Column('ID', Integer, primary_key=True),
                             Column('Name', String))

        self.sector_it_table = Table('Sector - it', metadata,
                                Column('Sector', Integer, primary_key=True),
                                Column('IT', String))

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        metadata.create_all(self.engine)

        mapper(It, self.it_table)
        mapper(Nko, self.nko_table)
        mapper(Moderator, self.moderator_table)
        mapper(Task, self.task_table)
        mapper(Sector, self.sector_table)
        mapper(Sector_It, self.sector_it_table)

    def create_it_person(self, id, surname, name):
        insert = self.it_table.insert(bind=self.engine)
        compiled = insert.compile()
        insert.execute(id, surname, name)


    # def create_nko_person(self, ):
    #     self.cur.execute(""" INSERT INTO "ПРЕДСТАВИТЕЛЬ НКО" VALUES (id, surname, name); """)
    #
    # def create_moderator(self, ):
    #     self.cur.execute(""" INSERT INTO "МОДЕРАТОР" VALUES (id, surname, name); """)
    #
    # def get_spheres(self):
    #     """ выдает список сфер обязательно всегда в одном и том же порядке (сортируйте по id)"""
    #     # return ["Дизайн", "Создатель сайтов", "Аналитик", "Дата сайнтист"]
    #     return self.cur.execute(""" SELECT "НАЗВАНИЕ" FROM "СФЕРА"; """)
    #
    # def get_user_spheres(self, username):
    #     """"""
    #     return self.cur.execute(""" SELECT * FROM "СФЕРА - IT" WHERE ID=username; """)
    #
    # def add_spheres2user(self, username, list_id_spheres):
    #     for id_sphere in list_id_spheres:
    #         self.cur.execute(""" INSERT INTO “СФЕРА - IT” VALUES (id_sphere, username); """)
    #
    # def add_task(self, id_nko, id_sphere, description):
    #     return self.cur.execute(""" INSERT INTO “ЗАДАЧА” VALUES
    #                                 (SELECT COUNT(*) FROM "ЗАДАЧА", id_nko,
    #                                 id_sphere, id_it = None, description, condition = 1) """)
    #
    # def get_tasks4moderator(self):
    #     return self.cur.execute(""" SELECT * FROM “ЗАДАЧА” WHERE “ЗАДАЧА”."СОСТОЯНИЕ" = 1 """)
    #
    # def update_condition_task(self, selected_task, condition):
    #     """если задачу на доработку, то передать 2, иначе 3"""
    #     self.cur.execute(""" UPDATE “ЗАДАЧА" SET "СОСТОЯНИЕ"=condition WHERE ID=selected_task """)
    #
    # def update_task(self, selected_task, id_sphere, description):
    #     self.cur.execute(""" UPDATE “ЗАДАЧА" SET "СОСТОЯНИЕ" = 1,
    #                          "СФЕРА" = id_sphere, "ОПИСАНИЕ" = description WHERE
    #                          ID = selected_task(?); """)
    #
    # def get_task4it(self):
    #     self.cur.execute(""" SELECT ЗАКАЗЧИК, СФЕРА.НАЗВАНИЕ, ОПИСАНИЕ FROM ЗАДАЧА, СФЕРА
    #                          JOIN  "СФЕРА - IT" ON  "СФЕРА - IT"."СФЕРА" = СФЕРА.ID
    #                          WHERE  СФЕРА.ID = ЗАДАЧА.СФЕРА AND
    #                          "СФЕРА - IT"."ПРЕДСТАВИТЕЛЬ IT" = id_it
    #                          ;""")
    #
    # def select_task(self, id_it, selected_task):
    #     self.cur.execute(""" UPDATE "ЗАДАЧИ" SET "СОСТОЯНИЕ"=4, "ИСПОЛНИТЕЛЬ"=id_it WHERE ID=selected_task; """)
    #
    # def submit_task(self, selected_task):
    #     self.cur.execute(""" UPDATE "ЗАДАЧИ" SET "СОСТОЯНИЕ"=5 WHERE ID=selected_task; """)
    #
    # def get_condition4nko(self, id_nko):
    #     return self.cur.execute(""" SELECT ИСПОЛНИТЕЛЬ, ОПИСАНИЕ, СОСТОЯНИЕ FROM "ЗАДАЧИ" WHERE "ЗАКАЗЧИК"=id_nko; """)
    #
    # def delete_it(self, id_it):
    #     self.cur.execute(""" DELETE FROM "ПРЕДСТАВИТЕЛЬ IT" WHERE ID = id_it;
    #                          UPDATE “ЗАДАЧА" SET "СОСТОЯНИЕ"=3
    #                          WHERE ИСПОЛНИТЕЛЬ = id_it;
    #                          DELETE FROM "СФЕРА - IT" WHERE "ПРЕДСТАВИТЕЛЬ IT" = id_it; """)
    #
    # def delete_nko(self, id_nko):
    #     self.cur.execute(""" DELETE FROM "ПРЕДСТАВИТЕЛЬ НКО" WHERE ID = id_nko;
    #                          DELETE FROM "ЗАДАЧА" WHERE "ЗАКАЗЧИК" = id_nko; """)
    #
    # def delete_moderator(self, id_moderator):
    #     self.cur.execute(""" DELETE FROM "МОДЕРАТОР" WHERE ID = id_moderator; """)
    #
    # def update_sphere(self):
    #     self.cur.execute(""" DELETE FROM "СФЕРА - IT" WHERE "ПРЕДСТАВИТЕЛЬ IT" = id_it;
    #                          INSERT INTO "СФЕРА - IT" VALUES
    #                          (id_sphere, id_it); """)


bot_db = Database()