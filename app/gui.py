import tkinter as tk
from tkinter import ttk, messagebox
from .monitoring import Monitor
import threading
from pytz import all_timezones

class WorkStatusAgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Work Status Agent")
        self.root.geometry("600x600")  # Increased window size
        self.root.configure(bg="#f0f0f0")
        self.monitor = None

        self.build_gui()

    def build_gui(self):
        # Apply a theme
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Styles with Larger Font Sizes
        style.configure('TLabel', font=('Helvetica', 14), padding=5, background="#f0f0f0") 
        style.configure('TEntry', font=('Helvetica', 14), padding=5) 
        style.configure('TButton', font=('Helvetica', 14), padding=5, background="#4CAF50", foreground="white") 
        style.configure('TCheckbutton', font=('Helvetica', 14), padding=5, background="#f0f0f0") 
        style.configure('TCombobox', font=('Helvetica', 14)) 

        # Frame for Configuration
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=(10, 10))
        config_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Screenshot Interval
        ttk.Label(config_frame, text="Screenshot Interval (minutes):").grid(row=0, column=0, sticky="w")
        self.interval_var = tk.IntVar(value=1)
        ttk.Entry(config_frame, textvariable=self.interval_var).grid(row=0, column=1, pady=5, padx=5) 

        # S3 Bucket Name
        ttk.Label(config_frame, text="S3 Bucket Name:").grid(row=1, column=0, sticky="w")
        self.s3_bucket_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.s3_bucket_var).grid(row=1, column=1, pady=5, padx=5)

        # AWS Access Key
        ttk.Label(config_frame, text="AWS Access Key:").grid(row=2, column=0, sticky="w")
        self.aws_access_key_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.aws_access_key_var).grid(row=2, column=1, pady=5, padx=5)

        # AWS Secret Key
        ttk.Label(config_frame, text="AWS Secret Key:").grid(row=3, column=0, sticky="w")
        self.aws_secret_key_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.aws_secret_key_var, show="*").grid(row=3, column=1, pady=5, padx=5)

        # AWS Region
        ttk.Label(config_frame, text="AWS Region:").grid(row=4, column=0, sticky="w")
        self.aws_region_var = tk.StringVar(value="ap-south-1")
        ttk.Entry(config_frame, textvariable=self.aws_region_var).grid(row=4, column=1, pady=5, padx=5)

        # Timezone
        ttk.Label(config_frame, text="Timezone:").grid(row=5, column=0, sticky="w")
        self.timezone_var = tk.StringVar(value="Asia/Kolkata")
        timezone_combobox = ttk.Combobox(config_frame, textvariable=self.timezone_var, values=all_timezones, state='readonly')
        timezone_combobox.grid(row=5, column=1, pady=5, padx=5)

        # Capture Screenshots
        self.capture_screenshots_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Capture Screenshots", variable=self.capture_screenshots_var).grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky="w")

        # Buttons Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Start Monitoring Button
        self.start_button = ttk.Button(button_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(side="left", expand=True, fill="x", padx=5)

        # Stop Monitoring Button
        self.stop_button = ttk.Button(button_frame, text="Stop Monitoring", command=self.stop_monitoring, state="disabled")
        self.stop_button.pack(side="left", expand=True, fill="x", padx=5)

        # Clear Button
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_config)
        self.clear_button.pack(side="left", expand=True, fill="x", padx=5)

    def start_monitoring(self):
        config = {
            'interval': self.interval_var.get(),
            's3_bucket': self.s3_bucket_var.get(),
            'aws_access_key': self.aws_access_key_var.get(),
            'aws_secret_key': self.aws_secret_key_var.get(),
            'region_name': self.aws_region_var.get(),
            'timezone': self.timezone_var.get(),
            'capture_screenshots': self.capture_screenshots_var.get(),
        }

        # Validate Configuration
        if not all(config.values()):
            messagebox.showerror("Configuration Error", "Please fill in all configuration fields.")
            return

        self.monitor = Monitor(config)
        self.monitor.start_monitoring()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        messagebox.showinfo("Monitoring Started", "WorkStatusAgent monitoring has started.")

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop_monitoring()
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            messagebox.showinfo("Monitoring Stopped", "WorkStatusAgent monitoring has stopped.")
    
    def clear_config(self):
        #clear configuration using this....
        self.interval_var.set(5)
        self.s3_bucket_var.set("")
        self.aws_access_key_var.set("")
        self.aws_secret_key_var.set("")
        self.aws_region_var.set("ap-south-1")
        self.timezone_var.set("Asia/Kolkata")
        self.capture_screenshots_var.set(True)
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        if self.monitor:
            self.monitor.stop_monitoring()
            self.monitor = None
