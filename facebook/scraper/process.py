from utils.log import logger
from facebook.scraper.request_handler import fb_scraper
from facebook.scraper.scrap import fetch_data


def process(url):
    """
    The `process` function takes a URL as input, determines if it's a video or image content, calls a
    web scraper to fetch data, processes the HTML content to extract likes, and logs the process.

    :param url: The `process` function takes a URL as input and performs the following steps:
    :return: The function `process(url)` returns the scraped data if it is successfully extracted from
    the HTML content using `fetch_data()` function. If no scraped data is found in the HTML content, it
    returns an empty dictionary `{}`. If there is an error during the process of calling `fb_scraper`,
    processing the HTML content, or if no HTML content is received from `fb_scraper`, it returns
    """
    if "watch" in url or "videos" in url:
        content_type = "Video"
    else:
        content_type = "image"

    # Log URL reading
    logger.info(f"Reading URL: {url}")

    # Call fb_scraper and log the process
    try:
        html_content = fb_scraper(url)
        logger.info("Received response from fb_scraper.")
    except Exception as e:
        logger.error(f"Error occurred while calling fb_scraper: {e}")
        html_content = None

    # Process the html_content if it's not None
    if html_content:
        logger.info("Processing html_content to extract likes.")
        try:
            scrapedData = fetch_data(html_content, content_type)
            if scrapedData:
                logger.info(f"scrapedData: {scrapedData}")
                return scrapedData
            else:
                logger.warning("No scrapedData information found in the html_content.")
                return {}
        except Exception as e:
            logger.error(f"Error occurred while processing html_content: {e}")
    else:
        logger.error("No html_content received from fb_scraper.")
        return {}
