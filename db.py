import sqlite3


class DataBase:
    def __init__(self):
        connection = sqlite3.connect('theatre.sqlite3', check_same_thread=False)
        self.connection = connection

    def get_connection(self):
        return self.connection

    def __del__(self):
        self.connection.close()


class ActorsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS actors 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          name VARCHAR(50), 
                          surname VARCHAR(50), 
                          role VARCHAR(50), 
                          bio VARCHAR(1000)
                          )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, surname, role, bio):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO actors 
                          (name, surname, role, bio) 
                          VALUES (?,?,?,?)''', (name, surname, role, bio))
        cursor.close()
        self.connection.commit()

    def get(self, actor_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM actors WHERE id = ?''', (str(actor_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, role=None):
        cursor = self.connection.cursor()
        if role:
            cursor.execute("SELECT id, name, surname, role FROM actors WHERE role = ?", (role,))
        else:
            cursor.execute("SELECT id, name, surname, role FROM actors")
        rows = cursor.fetchall()
        return rows

    def exists(self, actor_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, surname, role FROM actors WHERE id = ?", (str(actor_id),))
        row = cursor.fetchone()
        return (True, row[0], row[1], row[2]) if row else (False,)

    def edit(self, actor_id, name, surname, role, bio):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE actors 
                          SET name = ?, surname = ?, role = ?, bio = ? 
                          WHERE id = ?''', (name, surname, role, bio, str(actor_id)))
        cursor.close()
        self.connection.commit()

    def delete(self, actor_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM actors WHERE id = ?''', (str(actor_id),))
        cursor.close()
        self.connection.commit()


class PerformancesModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS performances 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          title VARCHAR(50), 
                          genre VARCHAR(50), 
                          time VARCHAR(30), 
                          actors VARCHAR(200), 
                          description VARCHAR(1000)
                          )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, genre, time, actors, description):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO performances 
                          (title, genre, time, actors, description) 
                          VALUES (?,?,datetime(?),?,?)''', (title, genre, time, actors, description))
        cursor.close()
        self.connection.commit()

    def get(self, perf_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT id, title, genre, strftime('%d.%m.%Y %H:%M', time), 
        actors, description FROM performances WHERE id = ?''', (str(perf_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, genre=None):
        cursor = self.connection.cursor()
        if genre:
            cursor.execute('''SELECT id, title, genre, strftime('%d.%m.%Y %H:%M', time) 
                              FROM performances WHERE genre = ? ORDER BY time ASC''', (genre,))
        else:
            cursor.execute('''SELECT id, title, genre, strftime('%d.%m.%Y %H:%M', time) 
                              FROM performances ORDER BY time ASC''')
        rows = cursor.fetchall()
        return rows

    def exists(self, perf_id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT id, title, genre, strftime('%d.%m.%Y %H:%M', time) 
                          FROM performances WHERE id = ?''', (str(perf_id),))
        row = cursor.fetchone()
        return (True, row[0], row[1], row[2], row[3]) if row else (False,)

    def edit(self, perf_id, title, genre, time, actors, description):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE performances 
                          SET title = ?, genre = ?, time = datetime(?), actors = ?, description = ? 
                          WHERE id = ?''', (title, genre, time, actors, description, str(perf_id)))
        cursor.close()
        self.connection.commit()

    def delete(self, perf_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM performances WHERE id = ?', (str(perf_id),))
        cursor.close()
        self.connection.commit()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          username VARCHAR(50), 
                          password_hash VARCHAR(128), 
                          favourites VARCHAR(200)
                          )''')
        cursor.close()
        self.connection.commit()

    def insert(self, username, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (username, password_hash, favourites) 
                          VALUES (?,?,"")''', (username, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return (True, row[0], row[2], row[3]) if row else (False,)

    def edit(self, user_id, username, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users 
                          SET username = ?, password_hash = ? 
                          WHERE id = ?''', (username, password_hash, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get_favourites(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT favourites FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row[0]

    def edit_favourites(self, user_id, favourites):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users 
                          SET favourites = ? 
                          WHERE id = ?''', (favourites, str(user_id)))
        cursor.close()
        self.connection.commit()

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id),))
        cursor.close()
        self.connection.commit()
