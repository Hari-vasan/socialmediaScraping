import requests
from utils.log import logger


def fb_scraper(url):
    """
    The function `fb_scraper` sends a GET request to a specified URL with custom headers, saves the
    response HTML content to a file, and returns the text if the response status code is 200.

    :param url: The function `fb_scraper` you provided is a Python function that scrapes the HTML
    content of a given URL using the `requests` library. It sets custom headers for the request, makes
    the request to the URL, and saves the HTML content to a file named "htmlcontent.html" if
    :return: The function `fb_scraper` returns the HTML content of the response if the status code is
    200. If the status code is not 200, it returns an empty list. If an exception occurs during the
    process, it logs an error message and returns nothing.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
        response = requests.get(url, headers=headers)
        logger.info("Reqests as hit with api")
        if response.status_code == 200:
            logger.info("Response is 200")
            with open("htmlcontent.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            return response.text

        else:
            logger.warning(f"Response is {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Failed to hit a api: {str(e)}")
