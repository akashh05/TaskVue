import unittest
from unittest.mock import patch, MagicMock
from app.config.poller import ConfigPoller

class TestConfigPoller(unittest.TestCase):

    @patch('requests.get')
    def test_poll_successful_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        mock_get.return_value = mock_response

        def mock_callback(config):
            self.assertEqual(config, {'key': 'value'})

        poller = ConfigPoller('http://test-url', mock_callback, interval=1)
        poller.poll()

    @patch('requests.get')
    def test_poll_network_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        poller = ConfigPoller('http://test-url', lambda config: None, interval=1)
        poller.poll()

if __name__ == '__main__':
    unittest.main()
