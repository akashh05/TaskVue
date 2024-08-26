import threading
import requests
import time

class ConfigPoller:
    def __init__(self, url, callback, interval=60):
        """
        Initialize the ConfigPoller with a URL and a callback function.
        """
        self.url = url
        self.callback = callback
        self.interval = interval
        self.polling = False
        self.poll_thread = None

    def start_polling(self):
        """
        Start the polling process in a separate thread.
        """
        if not self.polling:
            self.polling = True
            self.poll_thread = threading.Thread(target=self.poll)
            self.poll_thread.start()
            print("Started polling configuration.")

    def stop_polling(self):
        """
        Stop the polling process.
        """
        if self.polling:
            self.polling = False
            if self.poll_thread.is_alive():
                self.poll_thread.join()
            print("Stopped polling configuration.")

    def poll(self):
        """
        Poll the configuration server at regular intervals.
        """
        while self.polling:
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    config = response.json()
                    self.callback(config)  # Trigger the callback with the updated config...
                time.sleep(self.interval)
            except Exception as e:
                print(f"Error polling configuration: {e}")
                time.sleep(5)  # wait for a sec before trying....
