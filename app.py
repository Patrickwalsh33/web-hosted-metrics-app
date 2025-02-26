from flask import Flask, jsonify
import logging
import os
import psutil  # For system monitoring
from lib_config.config import load_config

# Configure logging
LOG_FILE = os.path.join(os.path.dirname(__file__), 'lib_config', 'logs', 'application_logs.csv')
logger = logging.getLogger('SystemMonitorLogger')
logger.setLevel(logging.INFO)

# Create a file handler that logs messages to a CSV file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Create a custom formatter for CSV output
class CSVFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record, datefmt='%Y-%m-%d %H:%M:%S')
        return f"{record.asctime},{record.levelname},{record.getMessage()}"

# Set the formatter for the file handler
formatter = CSVFormatter()
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Create Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>System Monitoring Tool</h1>"

@app.route('/status')
def status():
    # Gather system metrics
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    running_processes = len(psutil.pids())
    
    # Log the metrics
    logger.info(f"CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%, Running Processes: {running_processes}")
    
    # Return the metrics as JSON
    return jsonify({
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'running_processes': running_processes
    })

if __name__ == "__main__":
    logger.info("Starting the System Monitoring Tool...")
    app.run(debug=True)  # Set debug=True for development
