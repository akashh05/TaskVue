import tkinter as tk
from tkinter import messagebox
from app.gui import WorkStatusAgentApp
import threading
import time

# Check the mock monitor class to avoid real monitoring
class MockMonitor:
    def __init__(self, config):
        self.config = config
        self.monitoring = False

    def start_monitoring(self):
        self.monitoring = True
        print("Mock monitoring started with config:", self.config)

    def stop_monitoring(self):
        self.monitoring = False
        print("Mock monitoring stopped.")

def run_gui_test():
    WorkStatusAgentApp.Monitor = MockMonitor

    # Initialize the Tkinter root
    root = tk.Tk()
    
    # the WorkStatusAgentApp instance
    app = WorkStatusAgentApp(root)
    
    def simulate_user_interaction():
        time.sleep(1)
        
        # this set a interval time to 1 minutes 
        app.interval_var.set(1)
        
        # Set the S3 Bucket Name
        app.s3_bucket_var.set("test-bucket")
        
        # Set the AWS Access Key
        app.aws_access_key_var.set("test-access-key")
        
        # Set the AWS Secret Key
        app.aws_secret_key_var.set("test-secret-key")
        
        # Set the AWS Region
        app.aws_region_var.set("us-west-2")
        
        # Set the Timezone
        app.timezone_var.set("Asia/Kolkata")
        
        # Start Monitoring
        app.start_button.invoke()
        
        time.sleep(2)
        
        # Stop Monitoring
        app.stop_button.invoke()
        
        time.sleep(2)
        
        # Clear Configuration
        app.clear_button.invoke()
        
        time.sleep(2)
        
        # Close the application
        root.quit()

    threading.Thread(target=simulate_user_interaction).start()
    
    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    run_gui_test()
