import streamlit as st
from login import Login
from company_db import CompanyDB
import pandas as pd
from admin import Admin
# Load users
# Login.loadUsers()
company_db = CompanyDB()

# Page config
st.set_page_config(page_title="Stock Tracker", page_icon="📈", layout="centered")

# Session init
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Stock Tracker App</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sign out
if st.session_state.user:
    with st.sidebar:
        st.markdown("## 👤 Logged in as")
        # st.markdown(f"**{st.session_state.user.username} ({st.session_state.role.title()})**")
        if st.button("🚪 Sign Out"):
            st.session_state.user = None
            st.session_state.role = None
            st.success("Signed out successfully!")
            st.rerun()

# Login / Signup UI
if not st.session_state.user:
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Login or Create Account")
            tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

            with tab1:
                st.markdown("#### Existing User Login")
                username = st.text_input("Username", key="signin_user")
                password = st.text_input("Password", type="password", key="signin_pass")
                if st.button("Sign In"):
                    user_obj = Login.signIn(username, password)
                    if isinstance(user_obj, str):
                        st.error(user_obj)
                    else:
                        st.session_state.user = user_obj
                        st.session_state.role = user_obj.role
                        # st.success(f"Welcome, {user_obj.username} ({user_obj.role})")
                        st.rerun()

            with tab2:
                st.markdown("#### Create New Account")
                username = st.text_input("Choose a Username", key="signup_user")
                password = st.text_input("Choose a Password", type="password", key="signup_pass")
                role = st.selectbox("Select Role", ["user", "admin"])
                if st.button("Sign Up"):
                    result = Login.signUp(username, password, role)
                    st.success(result)
                    st.rerun()

# User Dashboard
if st.session_state.user:
    user_obj = st.session_state.user

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## 🎉 Welcome to Your Dashboard!")

    if st.session_state.role == "user":
        st.subheader("📥 User Dashboard")
        option = st.sidebar.radio("Choose Action", ["Add to Portfolio", "View Portfolio", "Decrease Quantity", "Request Company", "View Requests"])

        if option == "Add to Portfolio":
            st.markdown("### ➕ Add to Portfolio")
            company = st.text_input("Company Name")
            qty = st.number_input("Quantity to Add", min_value=1, step=1)
            if st.button("Add"):
                result = user_obj.addToPortfolio(company, qty, company_db.getDB())
                st.success(result)
                # Login.saveUsers()

        elif option == "View Portfolio":
            portfolio = user_obj.viewPortfolio()
            if isinstance(portfolio, str) and "Portfolio Empty" not in portfolio:
                # Extract actual portfolio dict from user_obj
                portfolio_dict = user_obj._User__userPortfolio
                if portfolio_dict:
                    st.markdown(f"### {user_obj.username}'s Portfolio")
                    portfolio_df = pd.DataFrame(list(portfolio_dict.items()), columns=["Company", "Shares"])
                    st.table(portfolio_df)
                else:
                    st.info("No stocks in your portfolio yet.")
            else:
                st.info("Your portfolio is empty.")


        elif option == "Decrease Quantity":
            st.markdown("### ➖ Decrease Quantity in Portfolio")
            company = st.text_input("Company to Decrease")
            qty = st.number_input("Quantity to Decrease", min_value=1, step=1)
            if st.button("Decrease"):
                result = user_obj.deleteFromPortfolio(company, qty)
                st.success(result)
                # Login.saveUsers()

        elif option == "Request Company":
            st.markdown("### 📝 Request New Company")
            company = st.text_input("Company to Request")
            if st.button("Request"):
                st.success(user_obj.requestCompany(company))
                # Login.saveUsers()

        elif option == "View Requests":
            st.markdown("### 📨 Company Requests")
            requests = user_obj.viewRequests()
            if "→" in requests:
                st.code(requests)
            else:
                st.info("No company requests yet.")

    # Admin Dashboard
    elif st.session_state.role == "admin":
        st.subheader("🛠 Admin Dashboard")
        # This line should fix your problem:
        admin_obj = Admin(user_obj.username, user_obj.password)

        option = st.sidebar.radio("Admin Actions", ["Add Company", "Delete Company", "View All Companies"])

        if option == "Add Company":
            st.markdown("### ➕ Add Company")
            company = st.text_input("Company Name to Add")
            if st.button("Add Company"):
                db = company_db.getDB()
                result = admin_obj.addCompanyToCompanyDB(company, db)
                company_db._CompanyDB__saveDB(db)
                st.success(result)

        elif option == "Delete Company":
            st.markdown("### ❌ Delete Company")
            company = st.text_input("Company Name to Delete")
            if st.button("Delete Company"):
                db = company_db.getDB()
                result = admin_obj.deleteCompanyFromCompanyDB(company, db)
                company_db._CompanyDB__saveDB(db)
                st.success(result)


        elif option == "View All Companies":
            st.markdown("### 🏢 Registered Companies")
            db = company_db.getDB()
            if db:
                st.table({"Companies": list(db.keys())})
            else:
                st.info("No companies are registered yet.")

