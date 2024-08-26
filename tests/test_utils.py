import unittest
from unittest.mock import MagicMock, patch
from app.utils import upload_with_retry

class TestUtils(unittest.TestCase):

    @patch('app.utils.time.sleep', return_value=None)
    def test_upload_with_retry_success(self, mock_sleep):
        s3_client = MagicMock()
        s3_client.upload_file.return_value = True
        result = upload_with_retry(s3_client, 'test_path', 'test_bucket', 'test_object')
        self.assertTrue(result)
        s3_client.upload_file.assert_called_once()

    @patch('app.utils.time.sleep', return_value=None)
    def test_upload_with_retry_fail(self, mock_sleep):
        s3_client = MagicMock()
        s3_client.upload_file.side_effect = Exception("Upload failed")
        result = upload_with_retry(s3_client, 'test_path', 'test_bucket', 'test_object')
        self.assertFalse(result)
        self.assertEqual(s3_client.upload_file.call_count, 3)

if __name__ == '__main__':
    unittest.main()
