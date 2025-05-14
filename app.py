#############################################################################
# app.py
#
# Entrypoint for the fitness app — now includes login and signup routing.
#############################################################################

import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_workouts

# --- Initialize session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.rerun()
if "username" not in st.session_state:
    st.session_state.username = ""
    st.rerun()
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
    st.rerun()
if "show_login" not in st.session_state:
    st.session_state.show_login = False
    st.rerun()

# --- Welcome Page ---
def main_landing_page():
    st.title("Welcome to To Be Determined's Website!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign up with username"):
            st.session_state.show_signup = True
            st.session_state.show_login = False
            st.rerun()
    with col2:
        if st.button("Log in"):
            st.session_state.show_login = True
            st.session_state.show_signup = False
            st.rerun()

# --- User Dashboard ---
def display_dashboard():
    st.title("🏋️ Your Fitness Dashboard")

    # Logout button
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.show_signup = False
        st.session_state.show_login = False
        st.rerun()

    try:
        username = st.session_state.username  # Use username as user ID substitute
        get_user_profile(username)

        for posts in get_user_posts(username):
            display_post(posts['user_name'], posts['profile_picture'], posts['timestamp'], posts['content'], posts['image'])

        # Workouts
        workouts = get_user_workouts(username)
        display_recent_workouts(workouts)
        display_activity_summary(workouts)

        # GenAI advice
        st.title("Get Motivational Advice")
        if st.button("Get Advice"):
            advice_data = get_genai_advice(username=username)
            st.success("Here's your advice!")
            display_genai_advice(advice_data["timestamp"], advice_data["content"], advice_data["image"])

    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --- Routing Logic ---
if __name__ == '__main__':
    if st.session_state.logged_in:
        display_dashboard()
    elif st.session_state.show_signup:
        from pages.signup_page import signup_page
        signup_page()
    elif st.session_state.show_login:
        from pages.login_page import login_page
        login_page()
    else:
        main_landing_page()
