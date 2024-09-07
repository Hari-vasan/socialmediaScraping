import datetime
import os


def get_log_filename(date_str=None):
    LOGS_FOLDER = "logs"  # Set the correct path to your logs folder
    if date_str:
        try:
            # Parse the date from the request
            log_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            log_filename = f"socialmediascraping.log.{log_date}"
        except ValueError:
            return None  # Invalid date format
    else:
        # Use current day log if no date is provided
        log_filename = "socialmediascraping.log"

    return os.path.join(LOGS_FOLDER, log_filename)
