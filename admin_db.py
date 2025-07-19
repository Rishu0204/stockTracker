import json
import os

class AdminDB:
    def __init__(self, filename="admins.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)
        self.admins = self.loadAdmins()

    def loadAdmins(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def saveAdmins(self):
        with open(self.filename, "w") as f:
            json.dump(self.admins, f, indent=4)

    def addAdmin(self, username, password):
        if username in self.admins:
            return False
        self.admins[username] = {
            "password": password,
            "actions": []
        }
        self.saveAdmins()
        return True

    def verifyAdmin(self, username, password):
        if username not in self.admins:
            return "Admin does not exist"
        if self.admins[username]["password"] != password:
            return "Incorrect password"
        return "admin"

    def logAction(self, username, action):
        if username in self.admins:
            self.admins[username]["actions"].append(action)
            self.saveAdmins()
