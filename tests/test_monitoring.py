import unittest
from unittest.mock import patch, MagicMock
from app.monitoring import Monitor

class TestMonitor(unittest.TestCase):

    @patch('app.monitoring.boto3.client')
    def test_initialize_s3_client_success(self, mock_boto3_client):
        mock_boto3_client.return_value = MagicMock()
        config = {
            'aws_access_key': 'test_key',
            'aws_secret_key': 'test_secret',
            'region_name': 'us-west-2'
        }
        monitor = Monitor(config)
        s3_client = monitor.initialize_s3_client()
        self.assertIsNotNone(s3_client)

    @patch('app.monitoring.boto3.client')
    def test_initialize_s3_client_failure(self, mock_boto3_client):
        mock_boto3_client.side_effect = Exception("Initialization failed")
        config = {
            'aws_access_key': 'test_key',
            'aws_secret_key': 'test_secret',
            'region_name': 'us-west-2'
        }
        monitor = Monitor(config)
        s3_client = monitor.initialize_s3_client()
        self.assertIsNone(s3_client)

    @patch('app.monitoring.Monitor.track_activity')
    @patch('app.monitoring.Monitor.monitor')
    def test_activity_tracking(self, mock_monitor, mock_track_activity):
        config = {
            'aws_access_key': 'test_key',
            'aws_secret_key': 'test_secret',
            'region_name': 'us-west-2'
        }
        monitor = Monitor(config)
        monitor.start_monitoring()
        self.assertTrue(mock_monitor.called)
        self.assertTrue(mock_track_activity.called)

    @patch('app.monitoring.boto3.client')
    @patch('app.monitoring.Monitor.track_activity')
    @patch('app.monitoring.Monitor.monitor')
    def test_monitor_screenshot_taken(self, mock_monitor, mock_track_activity, mock_boto3_client):
        mock_boto3_client.return_value = MagicMock()
        config = {
            'interval': 1,
            'aws_access_key': 'test_key',
            'aws_secret_key': 'test_secret',
            'region_name': 'us-west-2',
            'capture_screenshots': True
        }
        monitor = Monitor(config)
        monitor.start_monitoring()
        self.assertTrue(mock_monitor.called)
        self.assertTrue(mock_track_activity.called)

    @patch('app.monitoring.Monitor.track_activity')
    @patch('app.monitoring.Monitor.monitor')
    def test_stop_monitoring(self, mock_monitor, mock_track_activity):
        config = {
            'aws_access_key': 'test_key',
            'aws_secret_key': 'test_secret',
            'region_name': 'us-west-2'
        }
        monitor = Monitor(config)
        monitor.start_monitoring()
        monitor.stop_monitoring()
        self.assertFalse(monitor.monitoring)

if __name__ == '__main__':
    unittest.main()

