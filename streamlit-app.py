import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

# Veritabanı Bağlantısı
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

# Veritabanı Modeli
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


# Veritabanını Oluşturma
Base.metadata.create_all(bind=engine)

# Streamlit Oturum Durumu
if "email" not in st.session_state:
    st.session_state.email = None


# Ana Sayfa
def show_home():
    st.title("Hoş Geldiniz!")
    st.write("Lütfen giriş yapın veya kayıt olun.")
    if st.button("Giriş Yap"):
        st.session_state.page = "login"
    if st.button("Kayıt Ol"):
        st.session_state.page = "register"


# Kayıt Sayfası
def show_register():
    st.title("Kayıt Ol")
    name = st.text_input("İsim")
    email = st.text_input("E-posta")
    password = st.text_input("Şifre", type="password")
    if st.button("Kayıt Ol"):
        user = User(name=name, email=email, password=password)
        db_session.add(user)
        try:
            db_session.commit()
            st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            st.session_state.page = "login"
        except Exception as e:
            db_session.rollback()
            st.error("Bu e-posta zaten kayıtlı.")


# Giriş Sayfası
def show_login():
    st.title("Giriş Yap")
    email = st.text_input("E-posta")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        user = db_session.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            st.session_state.email = email
            st.success("Giriş başarılı!")
            st.session_state.page = "dashboard"
        else:
            st.error("Hatalı e-posta veya şifre.")


# Dashboard Sayfası
def show_dashboard():
    st.title("Dashboard")
    user = db_session.query(User).filter_by(email=st.session_state.email).first()
    if user:
        st.write(f"Merhaba, {user.name}!")
        if st.button("Çıkış Yap"):
            st.session_state.email = None
            st.session_state.page = "home"
    else:
        st.error("Bir hata oluştu. Lütfen tekrar giriş yapın.")
        st.session_state.page = "login"


# Sayfa Yönlendirme
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "register":
    show_register()
elif st.session_state.page == "login":
    show_login()
elif st.session_state.page == "dashboard":
    if st.session_state.email:
        show_dashboard()
    else:
        st.session_state.page = "login"
