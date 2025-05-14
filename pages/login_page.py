import streamlit as st
from data_fetcher import user_sign_in_function

def login_page():
    st.title("Welcome")

    if st.button("Go back to Start"):
        st.session_state.show_login = False
        st.rerun()
        
    if st.button("Sign up"):
        st.session_state.show_signup = True
        st.rerun()



    if st.session_state.get("show_login"):
        st.markdown("### Log In")
         
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                st.info("Submitting...")
                if user_sign_in_function(username, password):
                    st.info("Logged in successfully!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
                

    