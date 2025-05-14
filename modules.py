#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
from data_fetcher import user_sign_in_function, user_sign_up_function
import streamlit as st
import matplotlib.pyplot as plt #Added for display_activity_summary()
import pandas as pd  #Added for display_activity_summary()

# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username="username_error", user_image='https://developers.google.com/static/maps/documentation/streetview/images/error-image-generic.png', timestamp='00-00-00 00:00:00', content='Error loading user content', post_image='https://developers.google.com/static/maps/documentation/streetview/images/error-image-generic.png'):
    from internals import create_component
    import streamlit as st
    """Displays a user's post.
    
        username: The user's username
        user_image: The user's profile picture
        timestamp: The post's upload date    
        content: The post's text content
        post_image: The post's image
    """

    clean_text = f"""
    <style>
        .column {{
            float: left;
            width: 50%;
        }}
        #profile_picture {{
            clip-path: circle();
            height: 50px;
            margin-bottom: 1vh;
        }}
        #posted_image {{
            margin-top: 5vh;
            object-fit: cover;
            width: 300px;
            height: 300px;
            border-radius: 50px;
            border-radius: calc( 2vw + 2vh);
        }}
        #post_content {{
            border-radius: 25px;
            background-color: #E6E6E6;
            padding-left: 20px;
            padding-right: 20px;
            overflow-y: auto;
            height: 30vh;
            width: 13vw;
        }}
        #timestamp {{
            color: #a6a4a4;
        }}
        .display-post-container{{
            margin-top: 3vh;
        }}
    </style>

    <div class='display-post-container'>
    <h2>{username}'s post</h2> 

    <div class='column' id='post'>
        <img src="{post_image}"  alt="{username}\'s post image" height="110px" id="posted_image">
    </div>
    <div class='column' id='post_contents'>
        <img src='{user_image}' alt='{username}\'s profile picture' id='profile_picture'>
        <div id='post_content'>
            <p>{content}</p>
        </div>
        <p id='timestamp'>Posted: {timestamp}</p>
    </div>
    </div>
    """
    
    st.markdown(clean_text, unsafe_allow_html=True)


def display_activity_summary(workouts_list):
    # All this code is AI generated from the following conversation: https://gemini.google.com/app/b834cca690b30ef4
    """Displays a summary of the user's workouts with pie chart, separate bar charts, and table with custom column names."""
    if not workouts_list:
        st.write('No workouts found.')
        return

    # Determine the number of workouts to display based on display_recent_workouts' logic
    num_workouts = len(workouts_list)
    if num_workouts <= 3:
        max_workouts = num_workouts
    else:
        max_workouts = 3

    # Prepare data for charts and table
    calories = [workout['calories_burned'] for workout in workouts_list[:max_workouts]]
    distances = [workout['distance'] for workout in workouts_list[:max_workouts]]
    steps = [workout['steps'] for workout in workouts_list[:max_workouts]]

    # Use the actual workout IDs as labels
    workout_labels = [workout['workout_id'] for workout in workouts_list[:max_workouts]]

    # Display pie chart for calories
    if calories:
        st.subheader("Calories Burned")
        fig0, ax0 = plt.subplots()
        wedges, texts, autotexts = ax0.pie(calories, labels=workout_labels, autopct='%1.1f%%', startangle=90)
        ax0.axis('equal')
        legend_labels = [f"{label} ({value})" for label, value in zip(workout_labels, calories)]
        ax0.legend(wedges, legend_labels, title="Calories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig0)

    # Display bar chart for distance
    if distances:
        st.subheader("Distance Travelled")
        fig1, ax1 = plt.subplots()
        bars1 = ax1.bar(workout_labels, distances)
        ax1.set_ylabel("Distance")
        legend_labels1 = [f"{label} ({value})" for label, value in zip(workout_labels, distances)]
        ax1.legend(bars1, legend_labels1, title="Distance", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig1)

    # Display bar chart for steps
    if steps:
        st.subheader("Steps Taken")
        fig2, ax2 = plt.subplots()
        bars2 = ax2.bar(workout_labels, steps)
        ax2.set_ylabel("Steps")
        legend_labels2 = [f"{label} ({value})" for label, value in zip(workout_labels, steps)]
        ax2.legend(bars2, legend_labels2, title="Steps", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        st.pyplot(fig2)

    # Display workout details in a table
    st.subheader("Workout Details")
    table_data = []
    for i, workout in enumerate(workouts_list[:max_workouts]):
        table_data.append([
            workout['workout_id'],  # Use workout_id for the first column
            workout['start_timestamp'],
            workout['end_timestamp'],
            str(workout['start_lat_lng']),
            str(workout['end_lat_lng'])
        ])

    # Create a DataFrame with custom column names
    df = pd.DataFrame(table_data, columns=["Workout ID", "Start Time", "End Time", "Start Coordinates", "End Coordinates"])

    st.table(df)


def display_recent_workouts(workouts_list = []):
    """Displays a maximum of the last 3 workouts.
    
        workouts_list: A list of the user's total workouts
    """
    import streamlit as st
    

    if not workouts_list:
        st.write('No workouts found.')
        return
    
    data = {}
    if len(workouts_list) <= 3:
        cols = st.columns(len(workouts_list)) # Create streamlit columns

        for i, workout in enumerate(workouts_list):
            with cols[i % 3]:
                data = {
                            f'WORKOUT_ID': workout['workout_id'],
                            f'WORKOUT_START': workout['start_timestamp'],
                            f'WORKOUT_END': workout['end_timestamp'],
                            f'WORKOUT_START_LAT_LNG': workout['start_lat_lng'],
                            f'WORKOUT_END_LAT_LNG': workout['end_lat_lng'],
                            f'WORKOUT_DISTANCE': workout['distance'],
                            f'WORKOUT_STEPS': workout['steps'],
                            f'WORKOUT_CALORIES': workout['calories_burned']
                        }
                html_code = f"""
                    <style>
                        /* Note that the CSS selector matches the HTML class name */
                        .custom-component-container {{
                            border: 2px solid black;
                            padding: 0px;
                            height: 70vh;
                            width: 80vw;
                        }}
                        .column{{
                            float:left;
                            width: 50%;
                        }}
                        #profile_picture{{
                            clip-path: circle();
                        }}
                        #posted_image{{
                            object-fit: cover;
                            width: 300px;
                            height: 300px;
                            border-radius: 50px;
                            border-radius: calc( 5vw + 5vh); /* will scale, maybe you find this usefull */
                        }}
                        #workout{{
                            border-radius: 25px;
                            background-color: #E6E6E6;
                            padding-left: 20px;
                            padding-right: 20px;
                            overflow-y:auto;
                            height: 50vh;
                            width: 10vw;
                            font-family: "Open Sans", sans-serif;
                        }}
                        #additional-info{{
                            color:#a6a4a4;
                            font-size: small;
                        }}
                        #lat-lng{{
                            font-size:x-small;
                        }}
                        #workout-id{{
                            font-size: small;
                        }}
                        grey-text{{
                            color: #a6a4a4;
                        }}
                    </style>


                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">

                    <div class="workout-container">
                        <h2 id="workout-id"><grey-text>Workout ID: </grey-text>{data['WORKOUT_ID']}</h2>
                        <div class="column" id="workout">
                            <p>Start time: {data['WORKOUT_START']}</p>
                            <p>End time: {data['WORKOUT_END']}</p>
                            <p>Distance Travelled: {data['WORKOUT_DISTANCE']}</p>
                            <p>Steps taken: {data['WORKOUT_STEPS']}</p>
                            <p>Calories burnt: {data['WORKOUT_CALORIES']}</p>
                            <p id="additional-info">Additional Information</p>
                            <p id="lat-lng">Starting Latitude/Longitude: {data['WORKOUT_START_LAT_LNG']}</p>
                            <p id="lat-lng">Ending Latitude/Longitude: {data['WORKOUT_END_LAT_LNG']}</p>
                        </div>
                    </div>"""
                st.markdown(html_code, unsafe_allow_html=True)
    else:
        workouts_list = workouts_list[:3]
        for i, workout in enumerate(workouts_list):
            with cols[i % 3]:
                data = {
                            f'WORKOUT_ID': ['workout_id'],
                            f'WORKOUT_START': ['start_timestamp'],
                            f'WORKOUT_END': ['start_timestamp'],
                            f'WORKOUT_START_LAT_LNG': ['start_lat_lng'],
                            f'WORKOUT_END_LAT_LNG': ['end_lat_lng'],
                            f'WORKOUT_DISTANCE': ['distance'],
                            f'WORKOUT_STEPS': ['steps'],
                            f'WORKOUT_CALORIES': ['calories_burned']
                }
                html_code = f"""
                <style>
                    /* Note that the CSS selector matches the HTML class name */
                    .custom-component-container {{
                        border: 2px solid black;
                        padding: 0px;
                        height: 70vh;
                        width: 80vw;
                    }}
                    .column{{
                        float:left;
                        width: 50%;
                    }}
                    #profile_picture{{
                        clip-path: circle();
                    }}
                    #posted_image{{
                        object-fit: cover;
                        width: 300px;
                        height: 300px;
                        border-radius: 50px;
                        border-radius: calc( 5vw + 5vh); /* will scale, maybe you find this usefull */
                    }}
                    #workout{{
                        border-radius: 25px;
                        background-color: #E6E6E6;
                        padding-left: 20px;
                        padding-right: 20px;
                        overflow-y:auto;
                        height: 80vh;
                        width: 20vw;
                        font-family: "Open Sans", sans-serif;
                    }}
                    #additional-info{{
                        color:#a6a4a4;
                        font-size: small;
                    }}
                    #lat-lng{{
                        font-size:x-small;
                    }}
                    #workout-id{{
                        font-size: small;
                    }}
                    grey-text{{
                        color: #a6a4a4;
                    }}
                </style>


                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">

                <div class="workout-container">
                    <h2 id="workout-id"><grey-text>Workout ID: </grey-text>{{WORKOUT_ID}}</h2>
                    <div class="column" id="workout">
                            <p>Start time: {data['WORKOUT_START']}</p>
                            <p>End time: {data['WORKOUT_END']}</p>
                            <p>Distance Travelled: {data['WORKOUT_DISTANCE']}</p>
                            <p>Steps taken: {data['WORKOUT_STEPS']}</p>
                            <p>Calories burnt: {data['WORKOUT_CALORIES']}</p>
                            <p id="additional-info">Additional Information</p>
                            <p id="lat-lng">Starting Latitude/Longitude: {data['WORKOUT_START_LAT_LNG']}</p>
                            <p id="lat-lng">Ending Latitude/Longitude: {data['WORKOUT_END_LAT_LNG']}</p>
                    </div>
                </div>"""
                st.markdown(html_code, unsafe_allow_html=True)
        
    pass


def display_genai_advice(timestamp, content, image):
    """
    Displays the GenAI-generated advice in a Streamlit app.
    
    Args:
        timestamp (str): The timestamp of the generated advice.
        content (str): The motivational quote or advice.
        image (str or None): The URL of a motivational image (if available).

    Returns:
        None
    """

    # Display timestamp and advice text (Without Emojis)
    st.write(f"**Timestamp:** {timestamp}")
    st.write(f"**Advice:** {content}")
    

    # Display image if available
    if image:
        st.image(image, caption="Stay Motivated!", use_container_width=True)
    else:
        st.write("_No image available._")
