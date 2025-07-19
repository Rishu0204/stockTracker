# 📈 StockTracker App

A simple terminal-based stock management and login system using Python. This project supports **User** and **Admin** roles, allowing sign-up, sign-in, and company data management (CRUD operations).

---

## 🧠 Features

### 👤 Users
- Sign Up and Sign In functionality
- Persistent storage in `user.json`

### 🔐 Admins
- Secure login via `admin.json`
- View all registered companies
- Add new companies
- Delete existing companies

### 🗃 Companies
- Stored persistently in `companyDB.json`
- Only admins can modify this data

---

## 🏗️ Project Structure

StockTracker/
│
├── main.py # Entry point: handles user interaction
├── login.py # Login/Signup logic
├── admin.py # Admin menu logic
├── company_db.py # Company database CRUD operations
│
├── user.json # Stores user credentials
├── admin.json # Stores admin credentials
├── companyDB.json # Stores company data

---

## ▶️ How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/StockTracker.git
   cd StockTracker
   
   streamlit run main.py
📄 Example Admin Credentials
To get started, you may add an admin entry manually in admin.json:

json
Copy
Edit
{
  "admin1": "1234"
}
🧪 Sample Usage
pgsql
Copy
Edit
=== Welcome ===
1. Sign Up
2. Sign In
3. Exit
Enter choice: 2
User Name: admin1
Password: 1234
Welcome To Stock Tracker!!!

--- ADMIN MENU ---
1. View All Companies
2. Add New Company
3. Delete Company
4. Logout
💡 Future Improvements
Use of AI to get market updates and also to calculate profit or loss per stock

Company stock values and analytics

User portfolio tracking

Encrypted password storage

🧑‍💻 Author
Rishu Prasad
Oracle Certified Generative AI Professional | Python & Data Enthusiast
