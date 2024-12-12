# Flask User Management Application

Try here ! https://userdashboard.streamlit.app

## Overview
This is a Flask-based web application for managing user registration, login, and dashboard functionalities. It leverages Flask's simplicity and incorporates security features like password hashing using `bcrypt`. The application uses SQLite as its database backend.

## Features
1. User Registration: Users can sign up by providing their name, email, and password.
2. Secure Authentication: Passwords are securely hashed with bcrypt.
3. Session Management: Maintains user sessions for dashboard access.
4. User Dashboard: Displays user-specific details upon successful login.
5. Logout Functionality: Clears session data and redirects to the login page.

## Prerequisites and Installation
Ensure Python 3.7 or higher and Pip are installed on your system. Install dependencies using `pip install -r requirements.txt`. Initialize the database by running the following commands in a Python shell: `from app import db`, `db.create_all()`, and `exit()`. Start the Flask server by running `python app.py` and open your browser to `http://127.0.0.1:5000/`.

## File Structure
- app.py: Main application file containing routes and logic.
- templates/: Contains HTML templates for index, register, login, and dashboard.
- database.db: SQLite database file (auto-generated).

## Dependencies
See `requirements.txt` for a full list of dependencies: Flask, Flask-SQLAlchemy, bcrypt, Flask-WTF, Jinja2.

## Routes
1. `/` - Landing page
2. `/register` - Registration form
3. `/login` - Login form
4. `/dashboard` - User dashboard (requires authentication)
5. `/logout` - Logs out the user

## License
This project is open source and available under the MIT License.

## Sample Usage
Navigate to `/register` to create a new account, login with your credentials at `/login`, access your personalized dashboard at `/dashboard`, and logout using the `/logout` route.

**Author**: [irfansenyurt.com](http://irfansenyurt.com)


# Login page

![login](https://github.com/user-attachments/assets/023dda0d-5227-4ee8-8d69-e97b9eadaf1e)


# Register page
![register](https://github.com/user-attachments/assets/0d61bffe-a529-4bd4-836d-618dfb9dac56)



# Dashboard page

![dashboard](https://github.com/user-attachments/assets/637fa1af-89af-4afd-b77c-2b688234ea67)
