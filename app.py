import streamlit as st
import sqlite3
import bcrypt

# Database setup
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()

def register_user(name, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return user
    return None

# Streamlit app
st.title("User Login System")

menu = st.sidebar.selectbox("Menu", ["Home", "Register", "Login", "Dashboard", "Logout"])

if menu == "Home":
    st.write("Welcome to the User Login System!")

elif menu == "Register":
    st.subheader("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(name, email, password):
            st.success("Registration successful! Please log in.")
        else:
            st.error("Email already exists. Try logging in.")

elif menu == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state['user'] = user
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password.")

elif menu == "Dashboard":
    if 'user' in st.session_state:
        st.subheader("Dashboard")
        st.write(f"Welcome, {st.session_state['user'][1]}!")
        st.write("Here is your dashboard content.")
    else:
        st.warning("You need to log in to access the dashboard.")

elif menu == "Logout":
    if 'user' in st.session_state:
        del st.session_state['user']
        st.success("You have been logged out.")
        st.experimental_rerun()
