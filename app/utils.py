import time
import logging
import socket

logging.basicConfig(filename="app/assets/logs/workstatusagent.log", level=logging.INFO)

def upload_with_retry(s3_client, file_path, bucket_name, object_name, retries=3, delay=2):
    
    # This upload file to s3
    for attempt in range(retries):
        if not is_internet_available():
            logging.warning("No internet connection. Upload will retry when the connection is restored.")
            time.sleep(delay)
            continue

        try:
            s3_client.upload_file(file_path, bucket_name, object_name)
            logging.info(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
            return True
        except Exception as e:
            logging.error(f"Upload attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    return False

def check_firewall():
    
    # check Firewall function .....
    logging.info("Checking firewall status...")
    return True

def is_internet_available(host="8.8.8.8", port=53, timeout=3):
    
    # This can check a internet connnectivity....
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False
