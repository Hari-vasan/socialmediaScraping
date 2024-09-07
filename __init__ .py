from utils.log import logger
from instagram.scraper.scrap import fetch_data
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
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
            status_code=401,
        )
