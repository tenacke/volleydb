from mysql.connector import connect


class MySQLManager:
    def __init__(self):
        self.connection = connect(
            host="localhost",
            port=3306,
            database="volleydb1",
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor is not None:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection is not None:
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

    def get_teams(self):
        self.cursor.execute("SELECT * FROM team")
        teams = self.cursor.fetchall()
        self.cursor.reset()
        return teams
    
    def get_positions(self):
        self.cursor.execute("SELECT * FROM position")
        positions = self.cursor.fetchall()
        self.cursor.reset()
        return positions
    
    def add_player(self, username, password, name, surname, dob, height, weight, selected_teams, selected_positions):
        try:
            self.cursor.execute("INSERT INTO user(username, password, name, surname) VALUES (%s, %s, %s, %s)",
                                (username, password, name, surname))
            self.cursor.execute("INSERT INTO player(username, date_of_birth, height, weight) VALUES (%s, %s, %s, %s)",
                                (username, dob, height, weight))
            for team in selected_teams:
                self.cursor.execute("INSERT INTO playsforteam(username, team_id) VALUES (%s, %s)",
                                    (username, team))
            for position in selected_positions:
                self.cursor.execute("INSERT INTO playsinposition(username, position_id) VALUES (%s, %s)",
                                    (username, position))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Error occurred during player insertion:", e)
            raise
        finally:
            self.cursor.reset()
    
if __name__ == "__main__":
    manager = MySQLManager()
    print(manager.login("emre", "emre"))

