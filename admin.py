from admin_db import AdminDB
adminDBInstance = AdminDB()

class Admin: 
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = 'admin'

    def __normalizeDB(self, db):
        return {name.lower(): name for name in db}
    
    def addCompanyToCompanyDB(self, companyName, companyDB):
        try:
            companyName_lower = companyName.lower()
            normalizedDB = self.__normalizeDB(companyDB)

            if companyName_lower in normalizedDB:
                return f"'{normalizedDB[companyName_lower]}' is already registered."

            companyDB[companyName] = {}
            adminDBInstance.logAction(self.username, f"Added company '{companyName}'")
            return f"Company '{companyName}' added successfully."
        except Exception as e:
            return f"An error occurred: {e}"
    
    def deleteCompanyFromCompanyDB(self, companyName, companyDB):
        try:
            companyName_lower = companyName.lower()
            normalizedDB = self.__normalizeDB(companyDB)

            if companyName_lower not in normalizedDB:
                return "Company not registered."

            originalName = normalizedDB[companyName_lower]
            del companyDB[originalName]
            adminDBInstance.logAction(self.username, f"Deleted company '{originalName}'")
            return f"Company '{originalName}' deleted successfully."
        except Exception as e:
            return f"An error occurred: {e}"
        
    def viewAllCompanies(self, companyDB):
        try:
            if not companyDB:
                return "No companies registered."
            companies = "\nRegistered Companies:\n"
            for company in companyDB:
                companies += f"\n{company}\n"
            return companies.strip()
        except Exception as e:
            return f"An error occurred: {e}"
