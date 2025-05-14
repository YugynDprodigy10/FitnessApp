import streamlit as st
from modules import display_recent_workouts, display_activity_summary
from data_fetcher import get_user_workouts, get_user_profile, post_user_stat
from app import main_landing_page


def activity_page():
    st.title("Activity Page")

    username = st.session_state.username
    
    # Attempt to fetch user profile to validate the ID
    get_user_profile(username)

    # Get user's workouts
    workouts = get_user_workouts(username)

    st.header("Recent Workouts")
    display_recent_workouts(workouts)

    st.header("Activity Summary")
    display_activity_summary(workouts)

    # Share step count option
    total_steps = sum([w["steps"] for w in workouts if isinstance(w, dict) and "steps" in w])
    if st.button("Share my step count with the community"):
        content = f"Look at this, I walked {total_steps} steps today!"
        post_user_stat(username, content)
        st.success("Your activity has been shared with the community!")

if __name__ == '__main__':
    if st.session_state.logged_in:
        activity_page()
    elif st.session_state.show_signup:
        from pages.signup_page import signup_page
        signup_page()
    elif st.session_state.show_login:
        from pages.login_page import login_page
        login_page()
    else:
        main_landing_page()
