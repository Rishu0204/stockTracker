import json
import os

class CompanyDB:
    def __init__(self, filename="companies.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def __loadDB(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def __saveDB(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def __normalize(self, db):
        return {name.lower(): name for name in db}

    def addCompany(self, companyName):
        db = self.__loadDB()
        name_lower = companyName.lower()
        normalized = self.__normalize(db)
        if name_lower in normalized:
            return f"'{normalized[name_lower]}' already exists."
        db[companyName] = {}
        self.__saveDB(db)
        return f"'{companyName}' added successfully."

    def deleteCompany(self, companyName):
        db = self.__loadDB()
        name_lower = companyName.lower()
        normalized = self.__normalize(db)
        if name_lower not in normalized:
            return f"'{companyName}' not found."
        original = normalized[name_lower]
        del db[original]
        self.__saveDB(db)
        return f"'{original}' deleted successfully."

    def getAllCompanies(self):
        db = self.__loadDB()
        return list(db.keys())

    def isRegistered(self, companyName):
        db = self.__loadDB()
        return companyName.lower() in self.__normalize(db)

    def getDB(self):
        return self.__loadDB()
