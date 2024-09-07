import logging
import queue
import time
from logging.handlers import TimedRotatingFileHandler
import os


# Setup logging
logger = logging.getLogger("socialmediascraping.log")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    "logs/socialmediascraping.log",
    when="D",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Queue to store log messages
log_queue = queue.Queue()


def enqueue_log_message(message):
    """
    The function `enqueue_log_message` adds a message to a log queue.

    :param message: The `enqueue_log_message` function takes a `message` parameter, which is the log
    message that you want to add to the log queue
    """
    log_queue.put(message)


def process_log_queue():
    """
    The function `process_log_queue` continuously retrieves log messages from a queue and logs them
    using a logger at intervals of 1 second.
    """
    while True:
        if not log_queue.empty():
            log_message = log_queue.get()
            logger.info(log_message)
        time.sleep(1)


def log_stream(user_details):
    """
    The `log_stream` function generates log messages with user details and logs them while checking for
    new messages in a queue.

    :param user_details: The `log_stream` function takes a `user_details` parameter, which is expected
    to be a dictionary containing information about a user. The function then defines an inner generator
    function `generate` that continuously checks for log messages in a queue (`log_queue`), processes
    them by appending user details from the
    :return: The `log_stream` function returns a generator that continuously checks for log messages in
    a queue (`log_queue`). If a log message is found, it processes the message by appending the user's
    name from `user_details` to the log message and yields a formatted data string. The generator also
    logs the processed message using a logger.
    """

    def generate():
        while True:
            if not log_queue.empty():
                log_message = log_queue.get()
                user_log = (
                    str(log_message) + "--" + "user" + f"[{str(user_details['name'])}]"
                )
                yield f"data: {user_log}\n\n"
                logger.info(user_log)
            time.sleep(1)

    return generate()


def cleanup_old_logs(log_directory, days_old=7):
    """
    The function `cleanup_old_logs` deletes log files in a specified directory that are older than a
    certain number of days.

    :param log_directory: The `log_directory` parameter in the `cleanup_old_logs` function is the
    directory path where the log files are stored. This function will iterate through all files in this
    directory and delete files that are older than a specified number of days
    :param days_old: The `days_old` parameter in the `cleanup_old_logs` function specifies the number of
    days old a log file should be before it is considered for deletion. By default, it is set to 7 days,
    meaning any log file older than 7 days will be deleted when the function is called, defaults to 7
    (optional)
    """
    now = time.time()
    cutoff = now - days_old * 86400
    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)
        if os.path.isfile(file_path):
            file_time = os.path.getmtime(file_path)
            if file_time < cutoff:
                os.remove(file_path)
                print(f"Deleted old log file: {filename}")
