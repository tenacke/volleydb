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
        self.session_count = 0
        self.cursor.execute("SELECT MAX(session_id) FROM matchsession")
        self.session_count = self.cursor.fetchone()[0] + 1
        self.cursor.reset()

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

    def add_match_session(self, stadium, date, time_slot, jury, team_id):
        try:
            self.cursor.execute(
                "INSERT INTO matchsession(session_id, stadium_id, date, time_slot, assigned_jury_username, team_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (self.session_count, stadium, date, time_slot, jury, team_id),
            )
            self.connection.commit()
            self.session_count += 1
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()

    def delete_match_session(self, session_id):
        try:
            self.cursor.execute(
                "DELETE FROM matchsession WHERE session_id = %s;", (session_id,)
            )
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
        finally:
            self.cursor.reset()
        return True

    def add_squad(self, session_id, players):
        for player, position in players:
            try:
                self.cursor.execute(
                    "INSERT INTO sessionsquads(session_id, played_player_username, position_id) VALUES (%s, %s, %s)",
                    (session_id, player, position),
                )
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()
                raise
            finally:
                self.cursor.reset()

    def delete_squad(self, session_id):
        self.cursor.execute(
            "DELETE FROM sessionsquads WHERE session_id = %s;", (session_id,)
        )
        self.connection.commit()
        self.cursor.reset()

    def get_team_by_coach_username(self, coach_username, date):
        self.cursor.execute(
            """SELECT team_id FROM team WHERE coach_username = %s and contract_start <= STR_TO_DATE(%s, "%Y-%m-%d") and contract_finish >= STR_TO_DATE(%s, "%Y-%m-%d");""",
            (coach_username, date, date),
        )
        team = self.cursor.fetchone()
        self.cursor.reset()
        return team

    def get_sessions_by_coach_username(self, coach_username, filter):
        query = (
            """SELECT M.session_id, M.team_id FROM matchsession M inner join team on M.team_id = team.team_id 
            WHERE session_id not in (select session_id from sessionsquads) and team.coach_username = %s;"""
            if filter
            else """SELECT M.session_id, M.team_id FROM matchsession M inner join team on M.team_id = team.team_id 
            and team.coach_username = %s;"""
        )
        self.cursor.execute(
            query,
            (coach_username,),
        )
        sessions = self.cursor.fetchall()
        self.cursor.reset()
        return sessions

    def get_players_by_session_id(self, session_id):
        query = """SELECT DISTINCT user.username, user.name, user.surname
        FROM user inner join player on user.username = player.username
        inner join (select team from playerteams 
        inner join (select team_id from matchsession where session_id = %s) as session 
        on playerteams.team = session.team_id) as team"""
        self.cursor.execute(query, (session_id,))
        players = self.cursor.fetchall()
        self.cursor.reset()
        return players

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
