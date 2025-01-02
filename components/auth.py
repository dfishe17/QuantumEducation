import streamlit as st
import yaml
from yaml.loader import SafeLoader
import bcrypt
import logging
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_auth():
    """Initialize authentication configuration"""
    try:
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'is_admin' not in st.session_state:
            st.session_state['is_admin'] = False
        if 'theme' not in st.session_state:
            st.session_state['theme'] = 'light'

        # Create config file only if it doesn't exist
        if not os.path.exists('config.yaml'):
            logger.info("Creating new authentication config")
            config = {
                'credentials': {
                    'usernames': {
                        'admin': {
                            'name': 'Admin User',
                            'email': 'admin@quantum-edu.com',
                            'password': bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt()).decode(),
                            'is_admin': True
                        },
                        'demo': {
                            'name': 'Demo User',
                            'email': 'demo@quantum-edu.com',
                            'password': bcrypt.hashpw('demo123'.encode(), bcrypt.gensalt()).decode(),
                            'is_admin': False
                        }
                    }
                }
            }
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            logger.info("Successfully created authentication config")
        else:
            with open('config.yaml') as file:
                config = yaml.load(file, Loader=SafeLoader)
                logger.info("Successfully loaded existing authentication config")

        return config
    except Exception as e:
        logger.error(f"Error in init_auth: {str(e)}")
        raise

def show_auth_page():
    """Display authentication page"""
    try:
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        st.title("Welcome to Quantum Computing Education Hub")

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            show_login()

        with tab2:
            show_signup()
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_auth_page: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")

def show_login():
    """Display login form"""
    try:
        config = init_auth()

        st.markdown("### Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if username in config['credentials']['usernames']:
                    stored_password = config['credentials']['usernames'][username]['password']
                    if bcrypt.checkpw(password.encode(), stored_password.encode()):
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = username
                        st.session_state['name'] = config['credentials']['usernames'][username]['name']
                        st.session_state['is_admin'] = config['credentials']['usernames'][username].get('is_admin', False)
                        logger.info(f"Successful login for user: {username}")
                        st.success(f"Welcome back, {st.session_state['name']}!")
                        st.rerun()
                    else:
                        logger.warning(f"Failed login attempt for username: {username}")
                        st.error("Invalid password")
                else:
                    st.error("Username not found")

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        st.error("An error occurred during login. Please try again.")

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def show_signup():
    """Display signup form"""
    try:
        with st.form("signup_form"):
            st.subheader("Create New Account")
            new_username = st.text_input("Username")
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            new_password_confirm = st.text_input("Confirm Password", type="password")

            if st.form_submit_button("Sign Up"):
                if not all([new_username, new_name, new_email, new_password, new_password_confirm]):
                    st.error("Please fill in all fields")
                    return

                if not is_valid_email(new_email):
                    st.error("Please enter a valid email address")
                    return

                if new_password != new_password_confirm:
                    st.error("Passwords do not match!")
                    return

                try:
                    with open('config.yaml') as file:
                        config = yaml.load(file, Loader=SafeLoader)

                    if new_username in config['credentials']['usernames']:
                        st.error("Username already exists!")
                        return

                    # Check if email is already registered
                    for user in config['credentials']['usernames'].values():
                        if user.get('email') == new_email:
                            st.error("Email already registered!")
                            return

                    # Hash the password
                    password_bytes = new_password.encode()
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password_bytes, salt)

                    # Add new user
                    config['credentials']['usernames'][new_username] = {
                        'name': new_name,
                        'email': new_email,
                        'password': hashed_password.decode(),
                        'is_admin': False
                    }

                    # Save updated config
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)

                    logger.info(f"New user registered: {new_username}")
                    st.success("Account created successfully! Please log in.")
                except Exception as e:
                    logger.error(f"Signup error: {str(e)}")
                    st.error(f"An error occurred during signup: {str(e)}")

    except Exception as e:
        logger.error(f"Error in show_signup: {str(e)}")
        st.error("An error occurred while loading the signup form.")

def show_admin_panel():
    """Display admin panel for managing users"""
    if not st.session_state.get('is_admin', False):
        st.error("Access denied. Admin privileges required.")
        return

    st.title("Admin Panel")
    st.subheader("User Management")

    try:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        users = config['credentials']['usernames']

        # Display user table
        user_data = []
        for username, data in users.items():
            user_data.append({
                "Username": username,
                "Name": data['name'],
                "Email": data['email'],
                "Is Admin": data.get('is_admin', False)
            })

        st.table(user_data)

    except Exception as e:
        logger.error(f"Admin panel error: {str(e)}")
        st.error("Error loading admin panel")

def show_logout():
    """Display logout button"""
    try:
        if st.sidebar.button("Logout"):
            logger.info(f"User logged out: {st.session_state.get('username')}")
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['is_admin'] = False
            st.rerun()
    except Exception as e:
        logger.error(f"Error in show_logout: {str(e)}")
        st.error("An error occurred during logout.")