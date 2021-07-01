import sqlite3


class DBModels:
    def __init__(self):
        self.con = sqlite3.connect("users.db")
        self.cur = self.con.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            username text not null,
            password text not null
        )""")
    
    def successfull_login(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username = (?) AND password = (?)", (username, password))
        return len(self.cur.fetchall()) == 1
    
    def username_available(self, username):
        self.cur.execute("SELECT * FROM users WHERE username = (?)", (username,))
        return len(self.cur.fetchall()) == 0
    
    def create_account(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        self.con.commit()
