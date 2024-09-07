from utils.log import logger
import json
from twitter.scraper.process import process
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    This Python Azure Function processes a HTTP request to extract a URL, process it, and return a
    response in JSON format.

    :param req: The `req` parameter in the `main` function is of type `func.HttpRequest`, which
    represents an HTTP request received by the Azure Function. It contains information such as the
    request method, headers, query parameters, and request body. The function processes the request to
    extract a URL either from the
    :type req: func.HttpRequest
    :return: The code snippet defines a Python Azure Function that processes a HTTP request. If a URL is
    provided in the query string or request body, it processes the URL using a `process` function,
    converts the response dictionary to JSON, and returns it as a HTTP response. If there is an error
    during processing, it returns a 500 status code with an error message. If no URL is provided, it
    """
    logger.info("Python HTTP trigger function processed a request.")

    url = req.params.get("url")
    if not url:
        try:
            req_body = req.get_json()
        except ValueError:
            logger.error("Invalid JSON in request body")
            return func.HttpResponse(
                "Invalid JSON format",
                status_code=400,
            )
        else:
            url = req_body.get("url")

    if url:
        try:
            response_dict = process(url)
            response = json.dumps(response_dict)
            logger.info(f"Processed URL: {url}, Response: {response}")
            return func.HttpResponse(response)
        except Exception as e:
            logger.error(f"Error processing URL: {url}, Exception: {str(e)}")
            return func.HttpResponse(
                "Error processing URL",
                status_code=500,
            )
    else:
        return func.HttpResponse(
            "Please provide a URL in the query string or request body.",
            status_code=400,
        )
