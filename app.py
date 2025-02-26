from flask import Flask, render_template, jsonify
import logging
import os
import psutil  # For system monitoring
import mysql.connector  # For MySQL connection
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

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host='patrickwalsh.mysql.pythonanywhere-services.com',  
        user='patrickwalsh',  
        password='yz3RMDCNDk.xpL.',  
        database='patrickwalsh$systemMetricsApp'  
    )

@app.route('/')
def index():
    # Gather system metrics
    ram_usage = psutil.virtual_memory().percent
    running_processes = len(psutil.pids())
    
    # Log the metrics
    logger.info(f"RAM Usage: {ram_usage}%, Running Processes: {running_processes}")
    
    # Render the index template with metrics
    return render_template('index.html', ram_usage=ram_usage, running_processes=running_processes)

@app.route('/metrics')
def metrics():
    # Gather system metrics for JSON response
    ram_usage = psutil.virtual_memory().percent
    running_processes = len(psutil.pids())
    
    # Insert data into the database
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO system_metrics (ram_usage, running_processes) VALUES (%s, %s)", (ram_usage, running_processes))
    db_connection.commit()
    cursor.close()
    db_connection.close()
    
    return jsonify({
        'ram_usage': ram_usage,
        'running_processes': running_processes
    })

if __name__ == "__main__":
    logger.info("Starting the System Monitoring Tool...")
    app.run(debug=True)  # Set debug=True for development
