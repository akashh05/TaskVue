import boto3
import threading
import time
import os
import pyautogui
from datetime import datetime
from pytz import timezone
from .utils import upload_with_retry, check_firewall, is_internet_available
import traceback
import atexit

class Monitor:
    def __init__(self, config):
        
        # application configuration settings 
        self.interval = config.get('interval', 1)  # Default to 1 minute
        self.s3_bucket = config.get('s3_bucket')
        self.aws_access_key = config.get('aws_access_key')
        self.aws_secret_key = config.get('aws_secret_key')
        self.region_name = config.get('region_name', 'ap-south-1')
        self.timezone = config.get('timezone', 'Asia/Kolkata')
        self.capture_screenshots = config.get('capture_screenshots', True)
        self.monitoring = False
        self.s3_client = self.initialize_s3_client()
        self.monitor_thread = None
        self.activity_thread = None
        self.last_activity_time = time.time()
        self.activity_threshold = 10  # seconds to consider as inactivity
        atexit.register(self.cleanup)

    def initialize_s3_client(self):
        # here you provide your aws credentials 
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region_name
            )
            return s3_client
        except Exception as e:
            print(f"Failed to initialize S3 client: {e}")
            return None

    def start_monitoring(self):
        
        #Start The process  and remove the thread...
        if not self.s3_client:
            print("S3 client is not initialized. Cannot start monitoring.")
            return

        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor)
            self.monitor_thread.start()
            self.activity_thread = threading.Thread(target=self.track_activity)
            self.activity_thread.start()
            print("Monitoring started.")

    def stop_monitoring(self):

        #stop monitoring process
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join()
            if self.activity_thread and self.activity_thread.is_alive():
                self.activity_thread.join()
            print("Monitoring stopped.")

    def monitor(self):

        #main monitoring which take interval at a time.
        while self.monitoring:
            if time.time() - self.last_activity_time > self.activity_threshold:
                print("No recent activity detected. Skipping screenshot.")
                time.sleep(5)  # Wait a bit before checking again
                continue

            try:
                if self.capture_screenshots:
                    if not is_internet_available():
                        print("No internet connection. Queuing screenshot for later upload.")
                        continue
                    
                    screenshot = pyautogui.screenshot()
                    timestamp = datetime.now(timezone(self.timezone)).strftime('%Y%m%d_%H%M%S')
                    screenshot_path = os.path.join("app/assets/screenshots", f"screenshot_{timestamp}.png")
                    screenshot.save(screenshot_path)

                    success = upload_with_retry(self.s3_client, screenshot_path, self.s3_bucket, f"screenshots/{timestamp}.png")
                    if success:
                        print(f"Screenshot taken and uploaded at {timestamp}")
                    else:
                        print(f"Failed to upload screenshot at {timestamp}. Retrying later.")
                time.sleep(self.interval * 60)  # this show interval in seconds
            except Exception as e:
                print(f"Error during monitoring: {traceback.format_exc()}")
                time.sleep(5)

    def track_activity(self):

        #track a user using mouse pointer...
        import pygetwindow as gw
        while self.monitoring:
            try:
                active_window = gw.getActiveWindow()
                if active_window:
                    print(f"Employee Active window: {active_window.title}")
                    self.last_activity_time = time.time()
            except Exception as e:
                print(f"Error tracking activity: {e}")
            time.sleep(1)  # Check activity every second

    def cleanup(self):
        
        if self.monitoring:
            self.stop_monitoring()
