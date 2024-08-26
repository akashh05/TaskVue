import boto3
import threading
import time
import os
import pyautogui
from datetime import datetime
from pytz import timezone
from .utils import upload_with_retry, check_firewall
import traceback

class Monitor:
    def __init__(self, config):
        """
        Initialize the Monitor with configuration settings.
        """
        self.interval = config.get('interval', 1)  # This is default at 1. we can also change the value of this.
        self.s3_bucket = config.get('s3_bucket')
        self.aws_access_key = config.get('aws_access_key')
        self.aws_secret_key = config.get('aws_secret_key')
        self.region_name = config.get('region_name', 'ap-south-1')
        self.timezone = config.get('timezone', 'UTC')
        self.capture_screenshots = config.get('capture_screenshots', True)
        self.monitoring = False
        self.s3_client = self.initialize_s3_client()
        self.monitor_thread = None
        self.activity_thread = None
        self.last_activity_time = time.time()
        self.activity_threshold = 10  # seconds to consider as inactivity

    def initialize_s3_client(self):
        """
        Initialize the S3 client with provided credentials.
        """
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
        """
        Start the monitoring process in a separate thread.
        """
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
        """
        Stop the monitoring process.
        """
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread.is_alive():
                self.monitor_thread.join()
            if self.activity_thread.is_alive():
                self.activity_thread.join()
            print("Monitoring stopped.")

    def monitor(self):
        """
        The main monitoring loop that takes screenshots at regular intervals.
        """
        while self.monitoring:
            if time.time() - self.last_activity_time > self.activity_threshold:
                print("No recent activity detected. Skipping screenshot.")
                time.sleep(5)  # Wait a bit before checking again
                continue

            try:
                if self.capture_screenshots:
                    screenshot = pyautogui.screenshot()
                    timestamp = datetime.now(timezone(self.timezone)).strftime('%Y%m%d_%H%M%S')
                    screenshot_path = os.path.join("app/assets/screenshots", f"screenshot_{timestamp}.png")
                    screenshot.save(screenshot_path)

                    upload_with_retry(self.s3_client, screenshot_path, self.s3_bucket, f"screenshots/{timestamp}.png")
                    print(f"Screenshot taken and uploaded at {timestamp}")
                time.sleep(self.interval * 60)  # this can change every minutes in seconds
            except Exception as e:
                print(f"Error during monitoring: {traceback.format_exc()}")
                time.sleep(5)  

    def track_activity(self):
        """
        Track user activity such as mouse movement or keyboard input.
        """
        import pygetwindow as gw
        while self.monitoring:
            try:
                active_window = gw.getActiveWindow()
                if active_window:
                    print(f"Employee Active window: {active_window.title}")
                    self.last_activity_time = time.time()
            except Exception as e:
                print(f"Error tracking activity: {e}")
            time.sleep(1)  # This can check the employee in every second.
