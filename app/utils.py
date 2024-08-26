import time
import logging

logging.basicConfig(filename="app/assets/logs/workstatusagent.log", level=logging.INFO)

def upload_with_retry(s3_client, file_path, bucket_name, object_name, retries=3, delay=2):
    """
    Upload a file to S3 with retries.
    """
    for attempt in range(retries):
        try:
            s3_client.upload_file(file_path, bucket_name, object_name)
            logging.info(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
            return True
        except Exception as e:
            logging.error(f"Upload attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    return False

def check_firewall():
    """
    Placeholder function to check firewall status.
    """
    # this can check the firewall.
    logging.info("Checking firewall status...")
    return True

import time
import logging

logging.basicConfig(filename="app/assets/logs/workstatusagent.log", level=logging.INFO)

def upload_with_retry(s3_client, file_path, bucket_name, object_name, retries=3, delay=2):
    """
    Upload a file to S3 with retries.
    """
    for attempt in range(retries):
        try:
            # Uploading the screenshots to s3
            s3_client.upload_file(file_path, bucket_name, object_name)
            logging.info(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
            return True
        except Exception as e:
            logging.error(f"Upload attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    return False

