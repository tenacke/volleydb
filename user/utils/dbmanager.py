from mysql.connector import connect
from datetime import datetime


class MySQLManager:
    def __init__(self):
        self.connection = connect(
            host="localhost",
            port=3306,
            database="volleydb",
        )
        self.cursor = self.connection.cursor()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MySQLManager, cls).__new__(cls)
        return cls.instance

    def __del__(self):
        if hasattr(self, "cursor") and self.cursor is not None:
            self.cursor.close()
        if hasattr(self, "connection") and self.connection is not None:
            self.connection.close()

    def login(self, username, password):
        self.cursor.execute(
            "SELECT * FROM user WHERE username=%s AND password=%s", (username, password)
        )
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result

    def isCoach(self, username):
        self.cursor.execute("SELECT * FROM coach WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result is not None

    def isPlayer(self, username):
        self.cursor.execute("SELECT * FROM player WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result is not None

    def isJury(self, username):
        self.cursor.execute("SELECT * FROM jury WHERE username=%s", (username,))
        result = self.cursor.fetchone()
        self.cursor.reset()
        return result is not None

    def get_teams(self):
        self.cursor.execute("SELECT team_id, team_name FROM team")
        teams = self.cursor.fetchall()
        self.cursor.reset()
        return teams

    def get_positions(self):
        self.cursor.execute("SELECT * FROM position")
        positions = self.cursor.fetchall()
        self.cursor.reset()
        return positions

    def add_coach(self, username, password, name, surname, nationality):
        try:
            self.cursor.execute(
                "INSERT INTO user(username, password, name, surname) VALUES (%s, %s, %s, %s)",
                (username, password, name, surname),
            )
            self.cursor.execute(
                "INSERT INTO coach(username, nationality) VALUES (%s, %s)",
                (username, nationality),
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()

    def add_jury(self, username, password, name, surname, nationality):
        try:
            self.cursor.execute(
                "INSERT INTO user(username, password, name, surname) VALUES (%s, %s, %s, %s)",
                (username, password, name, surname),
            )
            self.cursor.execute(
                "INSERT INTO jury(username, nationality) VALUES (%s, %s)",
                (username, nationality),
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()

    def add_player(
        self,
        username,
        password,
        name,
        surname,
        dob,
        height,
        weight,
        selected_teams,
        selected_positions,
    ):
        try:
            self.cursor.execute(
                "INSERT INTO user(username, password, name, surname) VALUES (%s, %s, %s, %s)",
                (username, password, name, surname),
            )
            self.cursor.execute(
                "INSERT INTO player(username, date_of_birth, height, weight) VALUES (%s, %s, %s, %s)",
                (username, dob, height, weight),
            )
            for team in selected_teams:
                self.cursor.execute(
                    "INSERT INTO playerteams(username, team) VALUES (%s, %s)",
                    (username, team),
                )
            for position in selected_positions:
                self.cursor.execute(
                    "INSERT INTO playerpositions(username, position) VALUES (%s, %s)",
                    (username, position),
                )

            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()

    def get_stadiums(self):
        self.cursor.execute("SELECT * FROM stadium")
        stadiums = self.cursor.fetchall()
        self.cursor.reset()
        return stadiums

    def change_stadium_name(self, id, name):
        try:
            self.cursor.execute(
                "UPDATE stadium SET stadium_name = %s WHERE stadium_id = %s;",
                (name, id),
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()

    def average_ratings(self, username):
        self.cursor.execute(
            "SELECT AVG(rating) FROM matchsession WHERE assigned_jury_username = %s;",
            (username,),
        )
        average = self.cursor.fetchall()
        self.cursor.reset()
        return average[0][0]

    def count_ratings(self, username):
        self.cursor.execute(
            "SELECT COUNT(rating) FROM matchsession WHERE assigned_jury_username = %s;",
            (username,),
        )
        count = self.cursor.fetchall()
        self.cursor.reset()
        return count[0][0]

    def get_juries(self):
        self.cursor.execute(
            "SELECT user.username, user.name, user.surname FROM jury inner join user on jury.username = user.username"
        )
        juries = self.cursor.fetchall()
        self.cursor.reset()
        return juries

    def add_match_session(self, stadium, date, time_slot, jury):
        pass

    def delete_match_session(self, session_id):
        pass

    def add_squad(self, team_id, player_ids):
        pass

    def get_sessions_by_coach_username(self, coach_username):
        self.cursor.execute(
            """SELECT session_id FROM matchsession where session_id not in (select session_id from sessionsquad) 
            inner join team on matchsession.team_id = team.team_id WHERE team.coach_username = %s;""",
            (coach_username,),
        )

    def get_players_by_session_id(self, session_id):
        pass

    def get_rating_matches(self, username):
        current_date = datetime.now().date()
        sql_query = """SELECT * FROM matchsession 
        WHERE rating IS NULL AND assigned_jury_username = %s AND date < str_to_date(%s, "%Y-%m-%d")"""
        self.cursor.execute(sql_query, (username, current_date))
        matches = self.cursor.fetchall()
        self.cursor.reset()
        return matches

    def rate_match(self, id, rating):
        try:
            self.cursor.execute(
                "UPDATE matchsession SET rating = %s WHERE session_id = %s;",
                (rating, id),
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()

    def players(self, username):
        self.cursor.execute(
            """SELECT DISTINCT name, surname 
            FROM sessionsquads AS V1 
            INNER JOIN sessionsquads AS V2 ON V1.session_ID = V2.session_ID 
            INNER JOIN user ON V2.played_player_username = user.username 
            WHERE V1.played_player_username = %s AND V2.played_player_username != %s;""",
            (username, username),
        )
        players = self.cursor.fetchall()
        self.cursor.reset()
        return players

    def players_height(self, username):
        self.cursor.execute(
            """SELECT AVG(height) FROM
            (SELECT MAX(count) as max_count
            FROM (
            SELECT V2.played_player_username, COUNT(V2.played_player_username) AS count
            FROM sessionsquads AS V1 
            INNER JOIN sessionsquads AS V2 ON V1.session_ID = V2.session_ID 
            INNER JOIN user ON V2.played_player_username = user.username
            WHERE V1.played_player_username = %s AND V2.played_player_username != %s
            GROUP BY V2.played_player_username) AS all_counts) AS max_count
            INNER JOIN (SELECT V2.played_player_username, COUNT(V2.played_player_username) AS count
            FROM sessionsquads AS V1 
            INNER JOIN sessionsquads AS V2 ON V1.session_ID = V2.session_ID 
            INNER JOIN user ON V2.played_player_username = user.username
            WHERE V1.played_player_username = %s AND V2.played_player_username != %s
            GROUP BY V2.played_player_username) AS all_counts
            ON max_count = count
            INNER JOIN player ON played_player_username = username;""",
            (username, username, username, username),
        )
        height = self.cursor.fetchall()
        self.cursor.reset()
        return height[0][0]


if __name__ == "__main__":
    manager = MySQLManager()
