#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#############################################################################
import unittest
from unittest.mock import patch, Mock
from data_fetcher import get_user_sensor_data, get_user_workouts, get_user_profile, get_user_posts, get_genai_advice
import datetime



class TestDataFetcher(unittest.TestCase):

    def test_foo(self):
        """Tests foo."""
        pass

class TestDataFetcherPosts(unittest.TestCase):
    """Tests the get_user_posts function."""
    
    @patch('google.cloud.bigquery.Client')
    @patch('datetime.datetime')
    def test_get_user_posts_valid_user(self, MockDatetime, MockBigqueryClient):
        """Test with a valid user ID, ensuring correct data retrieval."""
        # 1. Setup Mocks
        mock_client = Mock()
        MockBigqueryClient.return_value = mock_client

        test_username = 'testuser'
        test_user_db_id = '1'  # The numerical user ID from the Users table
        test_author_id = f'user{test_user_db_id}' # The AuthorId format in Posts table

        # Mock the UserId query
        mock_user_id_job = Mock(name="UserIdJob")
        mock_user_id_job.result.return_value = [(test_user_db_id,)]

        # Create separate mock jobs for posts and profile queries
        mock_posts_job = Mock(name="PostsJob")
        mock_profile_job = Mock(name="ProfileJob")

        # Configure side_effect to return the specific jobs in order
        mock_client.query.side_effect = [mock_user_id_job, mock_posts_job, mock_profile_job]

        # Configure the posts job result
        mock_rows = [
            Mock(PostId='post1', AuthorId=test_author_id, Timestamp=datetime.datetime(2023, 1, 1, 10, 0, 0), ImageUrl='image1.jpg', Content='content1'),
            Mock(PostId='post2', AuthorId=test_author_id, Timestamp=datetime.datetime(2023, 1, 2, 11, 0, 0), ImageUrl='image2.jpg', Content='content2'),
        ]
        mock_posts_job.result.return_value = mock_rows

        # Configure the profile job mock to be ITERABLE
        mock_profile_row = Mock(Name='Test User 1', ImageUrl='http://example.com/user1.jpg')
        # Make the mock_profile_job itself yield the profile row when iterated
        mock_profile_job.__iter__ = Mock(return_value=iter([mock_profile_row]))
        mock_profile_job.result.return_value = [mock_profile_row] # Also set result for the loop

        # (Optional) Mock datetime if your function uses it directly
        MockDatetime.now.return_value = datetime.datetime(2025, 4, 19, 13, 25, 0)

        # 2. Call the function
        result = get_user_posts(test_username)

        # 3. Assertions
        self.assertEqual(len(result), 2)

        # Check post data AND profile data in the results
        self.assertEqual(result[0]['post_id'], 'post1')
        self.assertEqual(result[0]['user_id'], test_author_id)
        self.assertEqual(result[0]['timestamp'], datetime.datetime(2023, 1, 1, 10, 0, 0))
        self.assertEqual(result[0]['image'], 'image1.jpg')
        self.assertEqual(result[0]['content'], 'content1')
        self.assertEqual(result[0]['user_name'], 'Test User 1') # Verify profile data
        self.assertEqual(result[0]['profile_picture'], 'http://example.com/user1.jpg') # Verify profile data

        self.assertEqual(result[1]['post_id'], 'post2')
        self.assertEqual(result[1]['user_id'], test_author_id)
        self.assertEqual(result[1]['timestamp'], datetime.datetime(2023, 1, 2, 11, 0, 0))
        self.assertEqual(result[1]['image'], 'image2.jpg')
        self.assertEqual(result[1]['content'], 'content2')
        self.assertEqual(result[1]['user_name'], 'Test User 1') # Verify profile data (should be same)
        self.assertEqual(result[1]['profile_picture'], 'http://example.com/user1.jpg') # Verify profile data

        # Verify mock calls
        self.assertEqual(mock_client.query.call_count, 3)

        # Check arguments of calls using call_args_list
        expected_user_id_query = f"SELECT UserId FROM `ise-lab-1.ISE.Users` WHERE Username = '{test_username}'"
        expected_posts_query = f"SELECT * FROM `ise-lab-1.ISE.Posts` WHERE AuthorId = '{test_author_id}' LIMIT 100"
        expected_profile_query = f"SELECT Name, ImageUrl FROM `ise-lab-1.ISE.Users` WHERE Username = '{test_username}' LIMIT 100"

        self.assertEqual(mock_client.query.call_args_list[0][0][0], expected_user_id_query)
        self.assertEqual(mock_client.query.call_args_list[1][0][0], expected_posts_query)
        self.assertEqual(mock_client.query.call_args_list[2][0][0], expected_profile_query)

        # Verify result() was called on the posts job
        mock_posts_job.result.assert_called_once()
        mock_user_id_job.result.assert_called_once()
    
    @patch('google.cloud.bigquery.Client')
    def test_get_user_posts_no_posts(self, MockBigqueryClient):
        """Test when the user has no posts."""
        mock_client = Mock()
        MockBigqueryClient.return_value = mock_client

        test_username = 'charlieb'
        test_user_id = '123'  # Simulate the user ID found for 'charlieb'

        # Mock the UserId query result
        mock_user_id_query_job = Mock()
        mock_user_id_query_job.result.return_value = [(test_user_id,)]

        # Mock the Posts query result (empty for no posts)
        mock_posts_query_job = Mock()
        mock_posts_query_job.result.return_value = []

        # Mock the User profile query result
        mock_profile_query_job = Mock()
        mock_profile_row = Mock()
        mock_profile_row.Name = 'Charlie Brown'
        mock_profile_row.ImageUrl = 'http://example.com/charlie_profile.jpg'
        mock_profile_query_job.result.return_value = [mock_profile_row]

        # Configure the side effects for the query calls in the correct order
        mock_client.query.side_effect = [
            mock_user_id_query_job,
            mock_posts_query_job,
            mock_profile_query_job
        ]

        # Call the function
        result = get_user_posts(test_username)

        # Assertions
        self.assertEqual(result, [])  # Result should be an empty list

        # Verify the number of calls to client.query
        self.assertEqual(mock_client.query.call_count, 3)

        # Verify the arguments of each call
        expected_user_id_query = f"SELECT UserId FROM `ise-lab-1.ISE.Users` WHERE Username = '{test_username}'"
        mock_client.query.assert_any_call(expected_user_id_query)

        expected_posts_query = f"SELECT * FROM `ise-lab-1.ISE.Posts` WHERE AuthorId = 'user{test_user_id}' LIMIT 100"
        mock_client.query.assert_any_call(expected_posts_query)

        expected_profile_query = f"SELECT Name, ImageUrl FROM `ise-lab-1.ISE.Users` WHERE Username = '{test_username}' LIMIT 100"
        mock_client.query.assert_any_call(expected_profile_query)
    @patch('google.cloud.bigquery.Client')
    def test_get_user_posts_bigquery_error(self, MockBigqueryClient):
        """Test when BigQuery raises an exception."""
        mock_client = Mock()
        MockBigqueryClient.return_value = mock_client
        mock_client.query.side_effect = Exception("BigQuery Error")

        with self.assertRaises(Exception) as context:
            get_user_posts('charlieb')

        self.assertEqual(str(context.exception), "BigQuery Error")
        mock_client.query.assert_any_call("SELECT UserId FROM `ise-lab-1.ISE.Users` WHERE Username = 'charlieb'")

# Generated by Gemini: https://gemini.google.com/app/80dc4ea31e07a465
class TestDataFetcherWorkouts(unittest.TestCase):
    """Tests the get_user_workouts function."""

    @patch('google.cloud.bigquery.Client')
    def test_get_user_workouts_valid_user(self, MockBigqueryClient):
        """Test with a valid user ID, ensuring correct data retrieval."""
        # 1. Setup Mocks
        mock_client = Mock()
        MockBigqueryClient.return_value = mock_client

        test_username = 'testuser'
        test_user_internal_id = '5'  # Simulate the internal UserId from Users table

        # Mock the initial UserId query
        mock_user_id_job = Mock(name="UserIdJob")
        mock_user_id_job.result.return_value = [(test_user_internal_id,)]

        # Mock the workouts query
        mock_workouts_job = Mock(name="WorkoutsJob")
        mock_rows = [
            Mock(WorkoutId='workout1', StartTimestamp=datetime.datetime(2023, 1, 1, 8, 0, 0), EndTimestamp=datetime.datetime(2023, 1, 1, 9, 0, 0),
                StartLocationLat=30.0, StartLocationLong=-90.0, EndLocationLat=30.1, EndLocationLong=-90.1,
                TotalDistance=1.5, TotalSteps=2000, CaloriesBurned=300),
            Mock(WorkoutId='workout2', StartTimestamp=datetime.datetime(2023, 1, 2, 10, 0, 0), EndTimestamp=datetime.datetime(2023, 1, 2, 10, 30, 0),
                StartLocationLat=30.2, StartLocationLong=-90.2, EndLocationLat=30.3, EndLocationLong=-90.3,
                TotalDistance=0.8, TotalSteps=1000, CaloriesBurned=150),
        ]
        mock_workouts_job.result.return_value = mock_rows

        # Configure the side_effect to return the mock jobs in the correct order
        mock_client.query.side_effect = [mock_user_id_job, mock_workouts_job]

        # 2. Call the function (assuming get_user_workouts takes a username)
        result = get_user_workouts(test_username)

        # 3. Assertions
        self.assertEqual(len(result), 2)
        # ... (rest of your assertions for the workout data)

        # Verify mock calls
        self.assertEqual(mock_client.query.call_count, 2)

        expected_user_id_query = f"SELECT UserId FROM `ise-lab-1.ISE.Users` WHERE Username = '{test_username}'"
        expected_workouts_query = (
            "SELECT WorkoutId, StartTimestamp, EndTimestamp, StartLocationLat, "
            "StartLocationLong, EndLocationLat, EndLocationLong, TotalDistance, "
            f"TotalSteps, CaloriesBurned FROM ise-lab-1.ISE.Workouts WHERE UserId = '{'user' + test_user_internal_id}' "
        )
        mock_client.query.assert_any_call(expected_user_id_query)
        mock_client.query.assert_any_call(expected_workouts_query)


    @patch('google.cloud.bigquery.Client')
    def test_get_user_workouts_no_workouts(self, MockBigqueryClient):
        """Test when the user has no workouts."""

        # 1. Setup Mocks
        mock_client = Mock()
        MockBigqueryClient.return_value = mock_client
        mock_query_job = Mock()
        mock_client.query.return_value = mock_query_job
        mock_query_job.result.return_value = [] # No rows returned

        # 2. Call the function
        user_id_to_test = 'charlieb'
        result = get_user_workouts(user_id_to_test)

        # 3. Assertions
        self.assertEqual(result, []) # Should return an empty list
        expected_query = (
            "SELECT WorkoutId, StartTimestamp, EndTimestamp, StartLocationLat, StartLocationLong, EndLocationLat, EndLocationLong, TotalDistance, TotalSteps, CaloriesBurned FROM ise-lab-1.ISE.Workouts WHERE UserId = 'user0' "
        )
        mock_client.query.assert_any_call(f"SELECT UserId FROM `ise-lab-1.ISE.Users` WHERE Username = '{user_id_to_test}'")
        mock_client.query.assert_any_call(expected_query)
    

    @patch('google.cloud.bigquery.Client')
    def test_get_user_workouts_with_null_values(self, MockBigqueryClient):
        """Test when the user has workouts with some null values."""
        # 1. Setup Mocks
        mock_client = Mock()
        MockBigqueryClient.return_value = mock_client

        test_username = 'testuser'
        test_user_internal_id = '6'  # Simulate the internal UserId

        # Mock the initial UserId query
        mock_user_id_job = Mock(name="UserIdJob")
        mock_user_id_job.result.return_value = [(test_user_internal_id,)]

        # Mock the workouts query with null values
        mock_workouts_job = Mock(name="WorkoutsJob")
        mock_rows = [
            Mock(WorkoutId='workout3', StartTimestamp=datetime.datetime(2023, 1, 3, 9, 0, 0), EndTimestamp=None,
                 StartLocationLat=None, StartLocationLong=-90.5, EndLocationLat=30.6, EndLocationLong=None,
                 TotalDistance=2.0, TotalSteps=None, CaloriesBurned=400),
        ]
        mock_workouts_job.result.return_value = mock_rows

        # Configure the side_effect
        mock_client.query.side_effect = [mock_user_id_job, mock_workouts_job]

        # 2. Call the function
        result = get_user_workouts(test_username)

        # 3. Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['workout_id'], 'workout3')
        self.assertEqual(result[0]['end_timestamp'], None)
        self.assertIsInstance(result[0]['start_lat_lng'], tuple)
        # ... (rest of your assertions for null values)

        # Verify mock calls
        self.assertEqual(mock_client.query.call_count, 2)
        expected_user_id_query = f"SELECT UserId FROM `ise-lab-1.ISE.Users` WHERE Username = '{test_username}'"
        expected_workouts_query = (
            "SELECT WorkoutId, StartTimestamp, EndTimestamp, StartLocationLat, "
            "StartLocationLong, EndLocationLat, EndLocationLong, TotalDistance, "
            f"TotalSteps, CaloriesBurned FROM ise-lab-1.ISE.Workouts WHERE UserId = '{'user' + test_user_internal_id}' "
        )
        mock_client.query.assert_any_call(expected_user_id_query)
        mock_client.query.assert_any_call(expected_workouts_query)

# Generated by Gemini: https://gemini.google.com/app/80dc4ea31e07a465
class TestDataFetcherSensorData(unittest.TestCase):
  """Tests the get_user_sensor_data function."""

  @patch('google.cloud.bigquery.Client')
  def test_get_user_sensor_data_valid_data(self, MockBigqueryClient):
    """Test with valid user and workout IDs, ensuring correct data retrieval."""
    # 1. Setup Mocks
    mock_client = Mock()
    MockBigqueryClient.return_value = mock_client
    mock_query_job = Mock()
    mock_client.query.return_value = mock_query_job
    
    mock_rows = [
        Mock(
            SensorType='Heart Rate',
            Timestamp=datetime.datetime(2024, 7, 29, 7, 15, 0),
            SensorValue=120.0,
            Units='bpm',
        ),
        Mock(
            SensorType='Step Count',
            Timestamp=datetime.datetime(2024, 7, 29, 7, 30, 0),
            SensorValue=3000.0,
            Units='steps',
        ),
    ]
    mock_query_job.result.return_value = mock_rows

    # 2. Call the function
    user_id_to_test = 'user1'
    workout_id_to_test = 'workout1'
    result = get_user_sensor_data(user_id_to_test, workout_id_to_test)
    
    # 3. Assertions
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0]['sensor_type'], 'Heart Rate')
    self.assertEqual(
        result[0]['timestamp'], datetime.datetime(2024, 7, 29, 7, 15, 0)
    )
    self.assertEqual(result[0]['data'], 120.0)
    self.assertEqual(result[0]['units'], 'bpm')

    self.assertEqual(result[1]['sensor_type'], 'Step Count')
    self.assertEqual(
        result[1]['timestamp'], datetime.datetime(2024, 7, 29, 7, 30, 0)
    )
    self.assertEqual(result[1]['data'], 3000.0)
    self.assertEqual(result[1]['units'], 'steps')
    
    # Verify mock calls
    mock_client.query.assert_called_once()
    expected_query = "SELECT s.SensorType, s.Timestamp, s.SensorValue, st.Units FROM `ise-lab-1.ISE.SensorData` s JOIN `ise-lab-1.ISE.SensorTypes` st ON s.SensorId = st.SensorId WHERE s.WorkoutId = 'workout1' "
    mock_client.query.assert_called_once_with(expected_query)
 

  @patch('google.cloud.bigquery.Client')
  def test_get_user_sensor_data_no_data(self, MockBigqueryClient):
    """Test when there is no sensor data for the given workout."""
    # 1. Setup Mocks
    mock_client = Mock()
    MockBigqueryClient.return_value = mock_client
    mock_query_job = Mock()
    mock_client.query.return_value = mock_query_job
    mock_query_job.result.return_value = []  # No rows returned

    # 2. Call the function
    user_id_to_test = 'user2'
    workout_id_to_test = 'workout2'
    result = get_user_sensor_data(user_id_to_test, workout_id_to_test)

    # 3. Assertions
    self.assertEqual(result, [])  # Should return an empty list
    mock_client.query.assert_called_once()
    expected_query = "SELECT s.SensorType, s.Timestamp, s.SensorValue, st.Units FROM `ise-lab-1.ISE.SensorData` s JOIN `ise-lab-1.ISE.SensorTypes` st ON s.SensorId = st.SensorId WHERE s.WorkoutId = 'workout2' "
    mock_client.query.assert_called_once_with(expected_query)
 

  @patch('google.cloud.bigquery.Client')
  def test_get_user_sensor_data_bigquery_error(self, MockBigqueryClient):
    """Test when BigQuery raises an error."""
    # 1. Setup Mocks
    mock_client = Mock()
    MockBigqueryClient.return_value = mock_client
    mock_client.query.side_effect = Exception("BigQuery error")

    # 2. Call the function
    user_id_to_test = 'user3'
    workout_id_to_test = 'workout3'
    result = get_user_sensor_data(user_id_to_test, workout_id_to_test)

    # 3. Assertions
    self.assertEqual(result, [])  # Should return an empty list even with an error
    mock_client.query.assert_called_once()
    expected_query = "SELECT s.SensorType, s.Timestamp, s.SensorValue, st.Units FROM `ise-lab-1.ISE.SensorData` s JOIN `ise-lab-1.ISE.SensorTypes` st ON s.SensorId = st.SensorId WHERE s.WorkoutId = 'workout3' "
    mock_client.query.assert_called_once_with(expected_query)


if __name__ == "__main__":
    unittest.main()