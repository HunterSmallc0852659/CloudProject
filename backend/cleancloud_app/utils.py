import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_error(error):
    logging.error(f"Error: {error}")
