from utils.log import logger
from instagram.scraper.scrap import fetch_data
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    The function processes an HTTP request to fetch data from a specified URL and returns the response
    in JSON format.

    :param req: The `req` parameter in the `main` function is of type `func.HttpRequest`, which
    represents an HTTP request received by the Azure Function. It contains information such as the
    request method, headers, query parameters, and request body. The function processes this request to
    extract a URL either from the
    :type req: func.HttpRequest
    :return: The code snippet defines a Python Azure Function that processes HTTP requests. If a URL is
    provided in the query string or request body, it fetches data from that URL, converts the response
    to JSON, and returns it as an HTTP response. If there is an error during processing, it returns an
    error response with an appropriate status code. If no URL is provided, it returns a response asking
    for a
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
            response_dict = fetch_data(url)
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
