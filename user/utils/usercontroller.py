from .dbmanager import MySQLManager

class UserController:
    def __init__(self):
        self.manager = MySQLManager()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserController, cls).__new__(cls)
        return cls.instance

    def login(self, username, password):
        user = self.manager.login(username, password)
        print(user)
        if user is None:
            return None
        else:
            self.username = user[0]
            self.password = user[1]
            self.name = user[2]
            self.surname = user[3]

            if self.manager.isCoach(self.username):
                self.type = 'coach'
            elif self.manager.isPlayer(self.username):
                self.type = 'player'
            elif self.manager.isJury(self.username):
                self.type = 'jury'
            else:
                self.type = 'manager'

            return True