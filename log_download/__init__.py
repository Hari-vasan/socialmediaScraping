import logging
import os
import azure.functions as func
from log_download.get_log import get_log_filename


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Get the date parameter from the query string or body
    log_date = req.params.get("date")
    if not log_date:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            log_date = req_body.get("date")

    # Get the log file path
    log_file = get_log_filename(log_date)

    if log_file and os.path.exists(log_file):
        # If the log file exists, return the file content
        with open(log_file, "r") as file:
            file_content = file.read()
        return func.HttpResponse(file_content, mimetype="text/plain", status_code=200)
    elif log_date:
        # If log_date was provided but file is not found
        return func.HttpResponse(
            f"Log file for date {log_date} not available.", status_code=404
        )
    else:
        # No log_date and current log file not found
        return func.HttpResponse("Current log file not available.", status_code=404)
