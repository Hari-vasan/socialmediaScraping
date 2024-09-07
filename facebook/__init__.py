from utils.log import logger
from facebook.scraper.process import process
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    This Python Azure Function processes a HTTP request to extract a URL, process it, and return a
    response.

    :param req: The `req` parameter in the `main` function is of type `func.HttpRequest`, which
    represents an HTTP request received by the Azure Function. It contains information such as the
    request method, headers, query parameters, and request body. The function processes this request and
    returns a `func.HttpResponse
    :type req: func.HttpRequest
    :return: The `main` function returns an HTTP response based on the provided URL in the query string
    or request body.
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
