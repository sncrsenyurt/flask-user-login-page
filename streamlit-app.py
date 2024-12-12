import streamlit as st
import sqlite3
import bcrypt

# Veritabanı bağlantısı
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Kullanıcı tablosu oluştur
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# Kullanıcı kaydetme fonksiyonu
def register_user(name, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Kullanıcı giriş fonksiyonu
def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return user
    return None

# Streamlit UI
st.title("Kullanıcı Giriş ve Kayıt Sistemi")

menu = ["Giriş Yap", "Kayıt Ol"]
choice = st.sidebar.selectbox("Menü", menu)

if choice == "Kayıt Ol":
    st.subheader("Kayıt Ol")
    with st.form("register_form"):
        name = st.text_input("Adınız")
        email = st.text_input("E-posta")
        password = st.text_input("Şifre", type="password")
        submit_button = st.form_submit_button("Kayıt Ol")
    
    if submit_button:
        if register_user(name, email, password):
            st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
        else:
            st.error("Bu e-posta zaten kayıtlı.")

elif choice == "Giriş Yap":
    st.subheader("Giriş Yap")
    with st.form("login_form"):
        email = st.text_input("E-posta")
        password = st.text_input("Şifre", type="password")
        submit_button = st.form_submit_button("Giriş Yap")
    
    if submit_button:
        user = login_user(email, password)
        if user:
            st.success(f"Hoş geldiniz, {user[1]}!")
        else:
            st.error("Geçersiz e-posta veya şifre.")
