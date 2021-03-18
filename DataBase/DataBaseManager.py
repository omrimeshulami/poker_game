import sqlite3
from Enums import UserStatus


# TODO think later about multi threading and locks
class DataBaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('usersdatabase.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS 
                                    users(
                                    user_name TEXT NOT NULL PRIMARY KEY, 
                                    password TEXT NOT NULL,
                                    player_status TEXT NOT NULL,
                                    total_cash INTEGER NOT NULL,
                                    invested_cash INTEGER 
                                     
                                    )""")
        self.conn.commit()
        self.close_connection()

    def open_connection(self):
        self.conn = sqlite3.connect('usersdatabase.db')
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()
        self.cursor = None

    def register_user(self, username, password):
        self.open_connection()
        if not self.is_user_exist(username):
            self.cursor.execute("""
                                        INSERT INTO users VALUES
                                        (?,?,?,?,?)
                                        """, (username, password, UserStatus.OFFLINE.value, 5000, None))
            self.conn.commit()
            self.close_connection()
            return "Register Complete Successfully!"
        else:
            return "Username Already Been Taken, Please Try Another Username"

    def is_user_exist(self, username):
        self.open_connection()
        self.cursor.execute("SELECT * FROM users WHERE user_name=? ", (username,))
        if self.cursor.fetchone() == None:
            return False
        else:
            return True

    def delete_user(self, username):
        self.open_connection()
        if self.is_user_exist(username):
            self.cursor.execute("DELETE FROM users WHERE user_name=? ", (username,))
            self.conn.commit()
            self.close_connection()
            return "USER HAD BEEN DELETED"
        return "NO USER WITH THIS USERNAME"

    def login(self, username, password):
        self.open_connection()
        if self.is_user_exist(username):
            self.cursor.execute("SELECT * FROM users WHERE user_name=? ", (username,))
            user = self.cursor.fetchone()
            if user[0] == username and user[1] == password:
                self.cursor.execute("""UPDATE users 
                                       SET player_status=? 
                                       WHERE user_name=? """
                                    , (UserStatus.ONLINE.value, username))
                self.conn.commit()
                self.close_connection()
                return "Login Successfully!"
            else:
                return "Wrong PassWord"
        else:
            return "Error On Logging Out"

    # TODO will need to update cash on logout
    def logout(self, username):
        self.open_connection()
        if self.is_user_exist(username):
            user = self.cursor.fetchone()
            print(user)
            if user[0] == username:
                self.cursor.execute("""UPDATE users 
                       SET player_status=? 
                       WHERE user_name=? """
                                    , (UserStatus.OFFLINE.value, username))
                self.conn.commit()
                self.close_connection()
                return "Logout Successfully!"


manager = DataBaseManager()
manager.register_user("sssls", '1234')
print(manager.login("ssss", '1234'))
