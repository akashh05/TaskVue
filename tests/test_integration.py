import unittest
from unittest.mock import patch, MagicMock
from app.monitoring import Monitor
from app.config.poller import ConfigPoller

class TestIntegration(unittest.TestCase):

    @patch('app.monitoring.Monitor.start_monitoring')
    @patch('app.config.poller.requests.get')
    def test_monitor_with_config_update(self, mock_get, mock_start_monitoring):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'interval': 2,
            'aws_access_key': 'updated_key',
            'aws_secret_key': 'updated_secret',
            'region_name': 'us-west-2'
        }

        # start the configuration for the monitor
        config = {
            'interval': 1,
            'aws_access_key': 'test_key',
            'aws_secret_key': 'test_secret',
            'region_name': 'us-west-2'
        }
        monitor = Monitor(config)

        def callback(updated_config):
            print(f"Updated config: {updated_config}")
            monitor.__init__(updated_config)
            monitor.start_monitoring()

        poller = ConfigPoller('http://fakeurl.com', callback)
        
        with patch('time.sleep', return_value=None):
            poller.start_polling()

            poller.poll()

            mock_start_monitoring.assert_called_once()

if __name__ == '__main__':
    unittest.main()
