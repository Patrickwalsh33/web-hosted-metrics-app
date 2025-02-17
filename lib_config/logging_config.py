# lib_config/logging_config.py

import logging
import logging.handlers
import csv
import os

# Define the log file path to save it in the logs folder inside lib_config
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'application_logs.csv')

# Create a static logger object
logger = logging.getLogger('MyAppLogger')
logger.setLevel(logging.INFO)

# Create a file handler that logs messages to a CSV file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Create a custom formatter for CSV output
class CSVFormatter(logging.Formatter):
    def format(self, record):
        # Add asctime to the record
        record.asctime = self.formatTime(record, datefmt='%Y-%m-%d %H:%M:%S')
        # Create a CSV row using getMessage() to format the message
        return f"{record.asctime},{record.levelname},{record.getMessage()}"

# Set the formatter for the file handler
formatter = CSVFormatter()
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Ensure the log file has a header
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as csvfile:
        csvfile.write("Timestamp,Level,Message\n")