from user import User
from admin import Admin
from user_db import UserDB
from admin_db import AdminDB

userDBInstance = UserDB()
adminDBInstance = AdminDB()

class Login:
    @classmethod
    def signUp(cls, userName, password, role='user'):
        if role == 'admin':
            if not adminDBInstance.addAdmin(userName, password):
                return "Admin already exists"
            return f"Admin {userName} registered successfully"
        else:
            if not userDBInstance.addUser(userName, password, role):
                return "User already exists"
            return f"User {userName} registered successfully"

    @classmethod
    def signIn(cls, userName, password):
        # Check admin first
        role = adminDBInstance.verifyAdmin(userName, password)
        if role == "admin":
            return Admin(userName, password)
        elif role in ["Admin does not exist", "Incorrect password"]:
            # Try user
            role = userDBInstance.verifyUser(userName, password)
            if role in ["User does not exist", "Incorrect password"]:
                return role
            userData = userDBInstance.getUserData(userName)
            return User(userName, password, userData.get("portfolio"), userData.get("requests"))
        else:
            return role
