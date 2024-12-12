import streamlit as st
import sqlite3
import bcrypt

# Database connection
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

def register_user(name, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return user
    return None

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

st.title("User Login and Registration System")

if st.session_state.logged_in and st.session_state.user_info:
    # User dashboard
    st.title("user dashboard")
    st.write("**Name:**", st.session_state.user_info[1])
    st.write("**Email:**", st.session_state.user_info[2])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.experimental_rerun()
else:
    # If not logged in, show login or register forms
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Register")
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Register")

        if submit_button:
            if register_user(name, email, password):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("This email is already registered.")

    elif choice == "Login":
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

        if submit_button:
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_info = user
                st.experimental_rerun()
            else:
                st.error("Invalid email or password.")
