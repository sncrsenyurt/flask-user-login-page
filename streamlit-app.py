import streamlit as st
import sqlite3
import bcrypt

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

st.title("User Login and Registration System")

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
            st.success(f"Welcome, {user[1]}!")
        else:
            st.error("Invalid email or password.")
