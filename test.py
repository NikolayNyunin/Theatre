from db import DataBase, ActorsModel, PerformancesModel, UsersModel


db = DataBase()
actors_model = ActorsModel(db.get_connection())
actors_model.init_table()
performances_model = PerformancesModel(db.get_connection())
performances_model.init_table()
users_model = UsersModel(db.get_connection())
users_model.init_table()

performances_model.insert('Щелкунчик', 'Балет', '2019-04-26 16:00',
                          '1', 'Описание первого спектакля')
performances_model.insert('Евгений Онегин', 'Опера', '2019-04-26 20:00',
                          '2,3', 'Описание второго спектакля')
performances_model.insert('Травиата', 'Опера', '2019-04-27 16:00',
                          '2,3', 'Описание третьего спектакля')

actors_model.insert('Ольга', 'Иванова', 'Балерина', 'Биография первого актёра')
actors_model.insert('Иван', 'Петров', 'Певец', 'Биография второго актёра')
actors_model.insert('Дарья', 'Сидорова', 'Певица', 'Биография третьего актёра')
