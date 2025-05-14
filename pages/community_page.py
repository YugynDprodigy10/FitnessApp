#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from app import main_landing_page
from google.cloud import bigquery

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


def display_app_page():
    """Displays the home page of the app."""
    username = st.session_state.username
    st.title('Community')
    recent_posts = get_friends_posts(username)
    for posts in recent_posts:
        display_post(posts['user_name'], posts['profile_picture'], posts['timestamp'], posts['content'], posts['image'])
        
        
    st.title("Today's Motivational Advice:")
    advice_data = get_genai_advice(username)
    display_genai_advice(
    advice_data["timestamp"],
    advice_data["content"],
    advice_data["image"]
    )


def get_friends_posts(user):
    """Get the list of the 10 most recent posts by friends"""
    client = bigquery.Client()
    
    user_profile = get_user_profile(user)
    friend_posts_list = []
    for friend in user_profile['Friends']:
        USER_ID_QUERY = f"SELECT Username FROM `ise-lab-1.ISE.Users` WHERE UserId = '{friend[4:]}'"
        for row in client.query(USER_ID_QUERY).result():
            friend_username = row[0]
        for post in get_user_posts(friend_username):
            friend_posts_list.append(post)

    friend_posts_list = sorted(friend_posts_list, key=lambda item: item['timestamp']) 

    if len(friend_posts_list) > 10:
        friend_posts_list = friend_posts_list[:10]
    
    return friend_posts_list

 
if __name__ == '__main__':
    if st.session_state.logged_in:
        display_app_page()
    elif st.session_state.show_signup:
        from pages.signup_page import signup_page
        signup_page()
    elif st.session_state.show_login:
        from pages.login_page import login_page
        login_page()
    else:
        main_landing_page()