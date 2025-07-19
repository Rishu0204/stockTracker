from user_db import UserDB
from company_db import CompanyDB
from datetime import datetime
companyDBInstance = CompanyDB()
userDBInstance = UserDB()

class User:
    def __init__(self, userName, password, portfolio=None, requests=None,transactions=None):
        self.username = userName
        self.password = password
        self.role = 'user'
        self.__userPortfolio = portfolio or {}
        self.__requests = requests or {}
        self.__transactions = transactions or []

    def __save(self):
        userDBInstance.updateUserData(self.userName, {
            "portfolio": self.__userPortfolio,
            "requests": self.__requests,
            "transactions": self.__transactions 
        })


    def addToPortfolio(self, companyName, quantity, companyDB):
        try:
            if not companyDBInstance.isRegistered(companyName):
                return "Company not Registered"
            db = companyDBInstance.getDB()
            normalized = {name.lower(): name for name in db}
            originalName = normalized[companyName.lower()]

            self.__userPortfolio[originalName] = self.__userPortfolio.get(originalName, 0) + quantity
            self.__save()
            return f"Added {originalName} to {self.userName}'s portfolio"
        except Exception as e:
            return f"An error occurred: {e}"




    def viewPortfolio(self):
        if not self.__userPortfolio:
            return "Portfolio Empty!!"
        portfolio = f"{self.username}'s Portfolio:\n"
        for company, quantity in self.__userPortfolio.items():
            portfolio += f"{company}: {quantity}\n"
        return portfolio.strip()

    def requestCompany(self, companyName):
        try:
            if companyDBInstance.isRegistered(companyName):
                return f"{companyName.title()} is already registered."
            name_lower = companyName.lower()
            if name_lower in self.__requests:
                return f"You have already requested '{companyName}'."
            self.__requests[name_lower] = "Pending"
            self.__save()
            return f"Request to add '{companyName}' has been sent to the admin."
        except Exception as e:
            return f"An error occurred: {e}"

    def viewRequests(self):
        if not self.__requests:
            return "No pending requests."
        request_list = f"{self.userame}'s Requested Companies:\n"
        for company in self.__requests:
            request_list += f"{company.title()} → {self.__requests[company]}\n"
        return request_list.strip()
    
    def deleteFromPortfolio(self, companyName, quantity):
        try:
            normalized = {name.lower(): name for name in self.__userPortfolio}
            name_lower = companyName.lower()

            if name_lower not in normalized:
                return f"{companyName} not found in portfolio."

            originalName = normalized[name_lower]

            if quantity <= 0:
                return "Invalid quantity to sell."

            if self.__userPortfolio[originalName] < quantity:
                return f"You only own {self.__userPortfolio[originalName]} shares of {originalName}."

            self.__userPortfolio[originalName] -= quantity

            if self.__userPortfolio[originalName] == 0:
                del self.__userPortfolio[originalName]

            self.__save()  # persist changes
            return f"Sold {quantity} shares of {originalName}."
        except Exception as e:
            return f"An error occurred: {e}"

            
