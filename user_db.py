import json
import os

class UserDB:
    def __init__(self, filename="users.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)
        self.users = self.loadUsers()

    def loadUsers(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def saveUsers(self):
        with open(self.filename, "w") as f:
            json.dump(self.users, f, indent=4)

    def addUser(self, username, password, role="user"):
        if username in self.users:
            return False
        self.users[username] = {
            "password": password,
            "role": role,
            "portfolio": {},
            "transactions": [],
            "requests": {}
        }
        self.saveUsers()
        return True

    def verifyUser(self, username, password):
        if username not in self.users:
            return "User does not exist"
        if self.users[username]["password"] != password:
            return "Incorrect password"
        return self.users[username]["role"]

    def getUserData(self, username):
        return self.users.get(username)

    def updateUserData(self, username, user_data):
        if username in self.users:
            self.users[username].update(user_data)
            self.saveUsers()
