import streamlit as st
from data_fetcher import user_sign_up_function

def signup_page():
    st.title("Welcome")

    if st.button("Go back to Start"):
        st.session_state.show_signup = False
        st.rerun()

    if st.button("Log in"):
        st.session_state.show_signup = False
        st.session_state.show_login = True
        st.rerun()

    if st.session_state.get("show_signup"):
        st.markdown("### Sign Up")
        
        full_name = st.text_input("Please enter your full name")
        username = st.text_input("Please enter a username")
        password = st.text_input("Enter a safe Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        date_of_birth = st.date_input("Date of Birth", min_value='1900-01-01', format='YYYY-MM-DD')
        str(date_of_birth)

        if st.button("Create Account"):
            if password != confirm_password:
                st.error("Passwords do not match.")
            elif not username or not password or not date_of_birth:
                st.error("Please fill in all fields.")
            else:
                st.info("Submitting...")
                success = user_sign_up_function(full_name, username, password, date_of_birth=str(date_of_birth))
                if success == 'User created!':
                    st.info("Account created successfully! \n Please log in with your new credentials.")
                else:
                    st.warning(success)
