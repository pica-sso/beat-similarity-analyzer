"""
Advanced Logger utility.
Supports both session-based logging (for development) and daily logging.
"""

import logging
import os
import sys
from datetime import datetime

def setup_app_logger(name, log_to_session=True):
    """
    Configures a logger.
    :param name: Name of the logger.
    :param log_to_session: If True, creates a new log file for every run (HHMMSS).
                           If False, logs to a daily file (YYYY-MM-DD).
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    log_dir = os.path.join(root_dir, "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Choose filename format based on the mode
    if log_to_session:
        # e.g., 2026-01-25_221530.log (Every run gets a unique file)
        log_filename = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.log"
    else:
        # e.g., 2026-01-25.log (All runs in a day go to one file)
        log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"

    log_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if the logger is re-initialized
    if not logger.handlers:
        # Adding 'Session' prefix to format helps in identifying different runs
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

        # 1. File Handler
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 2. Console Handler (for PyCharm terminal)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger