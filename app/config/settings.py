class Settings:
    def __init__(self):
        self.config = {
            "interval": 5,
            "s3_bucket": "",
            "aws_access_key": "",
            "aws_secret_key": "",
            "region_name": "ap-south-1",
            "timezone": "Asia/Kolkata",
            "capture_screenshots": True,
        }

    def update(self, new_config):
        """
        Update the configuration settings.
        """
        self.config.update(new_config)
        print("Configuration updated:", self.config)

    def get(self, key):
        """
        Get a configuration value by key.
        """
        return self.config.get(key, None)
