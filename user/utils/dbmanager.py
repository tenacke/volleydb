from mysql.connector import connect

class MySQLManager:
    def __init__(self):
        self.connection = connect(
            host="localhost",
            port=3306,
            database="volleydb",
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def login(self, username, password):
        self.cursor.execute(
            "SELECT * FROM user WHERE username=%s AND password=%s",
            (username, password)
        )
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result
    
    def isCoach(self, username):
        self.cursor.execute(
            "SELECT * FROM coach WHERE username=%s",
            (username,)
        )
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result is not None
    
    def isPlayer(self, username):
        self.cursor.execute(
            "SELECT * FROM player WHERE username=%s",
            (username,)
        )
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result is not None
    
    def isJury(self, username):
        self.cursor.execute(
            "SELECT * FROM jury WHERE username=%s",
            (username,)
        )
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result is not None
    
    
if __name__ == "__main__":
    manager = MySQLManager()
    print(manager.login("emre", "emre"))

