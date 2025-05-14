#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
###########################################################################

import unittest
from unittest.mock import patch, MagicMock, mock_open, call #Added to test TestDisplayActivitySummary
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts
from data_fetcher import get_genai_advice


class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function.
        Mock tests were written with the assistance of Gemini AI"""
    def test_full_post(self):
        """Tests if Streamlit correctly displays a post with every argument."""
        with patch('streamlit.markdown') as mock_markdown:
            display_post(
                "Jimmy",
                "https://i.scdn.co/image/ab67616d00001e0257aacd72d8f523ddab7b5e48",
                "11:00:12 10-02-2025",
                "Im very excited about this watch so Im just writing about it here where I have free reign. ITS ABOUT TO COME OUT IM SO READY TO PRE-ORDERRRR. I really like e-paper",
                "https://platform.theverge.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/3729522/pebbletime2_2040.0.jpg?quality=90&strip=all&crop=0,0,100,100",
            )
    
            mock_markdown.assert_called_with(unittest.mock.ANY, unsafe_allow_html=True)

            args, kwargs = mock_markdown.call_args
            html_string = args[0]
            self.assertIn("<h2>Jimmy's post</h2>", html_string)
            self.assertIn("Im very excited about this watch so Im just writing about it here where I have free reign.", html_string)

    def test_empty_post(self):
        """Tests if Streamlit correctly displays an empty post."""
        with patch('streamlit.markdown') as mock_markdown:
            display_post()
            mock_markdown.assert_called_with(unittest.mock.ANY, unsafe_allow_html=True)
            args, kwargs = mock_markdown.call_args
            html_string = args[0]
            self.assertIn("Error loading user content", html_string)
        

class TestDisplayActivitySummary(unittest.TestCase):
    # These test were AI generated from the following conversation: https://gemini.google.com/app/b834cca690b30ef4
    """Tests the display_activity_summary function."""

    @patch('streamlit.write')
    @patch('streamlit.subheader')
    @patch('streamlit.pyplot')
    @patch('streamlit.table')
    def test_full_workout_set(self, mock_table, mock_pyplot, mock_subheader, mock_write):
        """Tests if Streamlit correctly displays a full workout set."""
        test_workout_list = [
            {'workout_id': 'workout0', 'start_timestamp': '2024-01-01 00:00:00', 'end_timestamp': '2024-01-01 00:30:00', 'start_lat_lng': (1.46, 4.03), 'end_lat_lng': (1.08, 4.18), 'distance': 11.5, 'steps': 8863, 'calories_burned': 77},
            {'workout_id': 'workout1', 'start_timestamp': '2024-01-01 00:00:00', 'end_timestamp': '2024-01-01 00:30:00', 'start_lat_lng': (1.25, 4.85), 'end_lat_lng': (1.3, 4.85), 'distance': 4.9, 'steps': 1936, 'calories_burned': 12},
            {'workout_id': 'workout2', 'start_timestamp': '2024-01-02 00:00:00', 'end_timestamp': '2024-01-02 00:30:00', 'start_lat_lng': (1.87, 4.31), 'end_lat_lng': (1.36, 4.56), 'distance': 7.3, 'steps': 5492, 'calories_burned': 45}
        ]
        display_activity_summary(test_workout_list)
        # Check if the table was called
        mock_table.assert_called_once()

    @patch('streamlit.write')
    def test_empty_workout_set(self, mock_write):
        """Tests if Streamlit correctly displays an empty workout set."""
        display_activity_summary([])
        # Check if st.write was called with the correct message
        mock_write.assert_called_once_with('No workouts found.')

    @patch('streamlit.write')
    @patch('streamlit.subheader')
    @patch('streamlit.pyplot')
    @patch('streamlit.table')
    def test_one_workout(self, mock_table, mock_pyplot, mock_subheader, mock_write):
        """Tests if Streamlit correctly displays a single workout."""
        test_workout_list = [
            {'workout_id': 'workout0', 'start_timestamp': '2024-01-01 00:00:00', 'end_timestamp': '2024-01-01 00:30:00', 'start_lat_lng': (1.46, 4.03), 'end_lat_lng': (1.08, 4.18), 'distance': 11.5, 'steps': 8863, 'calories_burned': 77},
        ]
        display_activity_summary(test_workout_list)
        # Check if the table was called
        mock_table.assert_called_once()

    @patch('streamlit.write')
    @patch('streamlit.subheader')
    @patch('streamlit.pyplot')
    @patch('streamlit.table')
    def test_more_than_three_workouts(self, mock_table, mock_pyplot, mock_subheader, mock_write):
        """Tests if Streamlit correctly displays more than three workouts."""
        test_workout_list = [
            {'workout_id': 'workout0', 'start_timestamp': '2024-01-01 00:00:00', 'end_timestamp': '2024-01-01 00:30:00', 'start_lat_lng': (1.46, 4.03), 'end_lat_lng': (1.08, 4.18), 'distance': 11.5, 'steps': 8863, 'calories_burned': 77},
            {'workout_id': 'workout1', 'start_timestamp': '2024-01-01 00:00:00', 'end_timestamp': '2024-01-01 00:30:00', 'start_lat_lng': (1.25, 4.85), 'end_lat_lng': (1.3, 4.85), 'distance': 4.9, 'steps': 1936, 'calories_burned': 12},
            {'workout_id': 'workout2', 'start_timestamp': '2024-01-02 00:00:00', 'end_timestamp': '2024-01-02 00:30:00', 'start_lat_lng': (1.87, 4.31), 'end_lat_lng': (1.36, 4.56), 'distance': 7.3, 'steps': 5492, 'calories_burned': 45},
            {'workout_id': 'workout3', 'start_timestamp': '2024-01-03 00:00:00', 'end_timestamp': '2024-01-03 00:30:00', 'start_lat_lng': (1.46, 4.03), 'end_lat_lng': (1.08, 4.18), 'distance': 11.5, 'steps': 8863, 'calories_burned': 77},
        ]
        display_activity_summary(test_workout_list)
        # Check if the table was called
        mock_table.assert_called_once()


class TestGenAIAdvice(unittest.TestCase):

    @patch("data_fetcher.vertexai.init")
    @patch("data_fetcher.get_user_profile")
    @patch("data_fetcher.GenerativeModel")
    def test_genai_advice_format(self, mock_model_class, mock_get_user_profile, mock_vertexai_init):
        # Mock user profile
        mock_get_user_profile.return_value = {
            "userID": "user1",
            "Name": "Remi",
            "Username": "remi_the_rems",
            "DateOfBirth": "1990-01-01",
            "ImageUrl": "https://someurl.com/pic.jpg",
            "Friends": []
        }

        # Set up mock for Gemini model
        mock_model_instance = MagicMock()
        
        # Ensure generate_content().text.strip() returns the expected string
        mock_generate_result = MagicMock()
        mock_generate_result.text.strip.return_value = "Keep pushing forward!"
        mock_model_instance.generate_content.return_value = mock_generate_result

        mock_model_class.return_value = mock_model_instance

        # Call the function
        result = get_genai_advice("user1")

        # DEBUG print (optional)
        print("DEBUG Final Result:", result)

        # Assert structure
        self.assertIn("advice_id", result)
        self.assertIn("timestamp", result)
        self.assertIn("content", result)
        self.assertIn("image", result)
        self.assertEqual(result["content"], "Keep pushing forward!")



class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""
    def test_full_workout_set(self):
        test_workout_list = [{'workout_id': 'workout0',
        'start_timestamp': '2024-01-01 00:00:00',
        'end_timestamp': '2024-01-01 00:30:00',
        'start_lat_lng': (1.46, 4.03),
        'end_lat_lng': (1.08, 4.18),
        'distance': 11.5,
        'steps': 8863,
        'calories_burned': 77},
        {'workout_id': 'workout1',
        'start_timestamp': '2024-01-01 00:00:00',
        'end_timestamp': '2024-01-01 00:30:00',
        'start_lat_lng': (1.25, 4.85),
        'end_lat_lng': (1.3, 4.85),
        'distance': 4.9,
        'steps': 1936,
        'calories_burned': 12}]

        with patch('streamlit.columns') as mock_columns, patch('streamlit.markdown') as mock_markdown:
            mock_col1 = MagicMock()

            mock_col2 = MagicMock()

            mock_columns.return_value = [mock_col1, mock_col2]

            display_recent_workouts(test_workout_list)

            mock_columns.assert_called_once()
            self.assertEqual(mock_markdown.call_count, 2)

            args1, kwargs1 = mock_markdown.call_args_list[0]
            markdown_string1 = args1[0]
            self.assertIn('11.5', markdown_string1)
            self.assertIn('Start time: 2024-01-01 00:00:00', markdown_string1)
            self.assertIn('workout0', markdown_string1)

            args2, kwargs2 = mock_markdown.call_args_list[1]
            markdown_string2 = args2[0]
            self.assertIn('4.9', markdown_string2)
            self.assertIn('workout1', markdown_string2)

    def test_empty_workout_set(self):
        """Tests if Streamlit correctly displays a post with an empty argument."""
        
        with patch('streamlit.write') as mock_write:
            display_recent_workouts([])
            self.assertTrue(mock_write.called)
            mock_write.assert_called_once_with('No workouts found.')


if __name__ == "__main__":
    unittest.main()
    


# Mocks

class MockInternals:
    def __init__(self):
        pass

    def create_component(self, data, html_file_name):

        pass