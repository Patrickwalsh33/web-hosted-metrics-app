# hello_world.py

from lib_config.config import load_config
from lib_config.logging_config import logger  # Import the static logger

def main():
    logger.info("Loading configuration...")
    config = load_config()
    logger.info("Configuration loaded successfully.")
    logger.info("Greeting: %s", config["greeting"])
    print(config["greeting"])

if __name__ == "__main__":
    main()
