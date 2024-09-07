from utils.log import logger
from twitter.scraper.extract_tweet_id import extract_tweet_id
from twitter.scraper.readGuestToken import readGuestTokentxt
from twitter.scraper.request_handler import scrape_tweet


def process(url):
    """
    The function processes a given URL by extracting a tweet ID, reading a guest token, and scraping
    tweet data, returning the scraped data or an empty dictionary in case of an exception.

    :param url: The `process` function takes a URL as input. It logs a message indicating that it is
    reading the provided URL. It then attempts to extract a tweet ID from the URL, read a guest token
    from a file, and scrape data from the tweet using the extracted tweet ID, URL, and guest
    :return: The function `process(url)` is returning the `scrapedData` if the process is successful. If
    an exception occurs during the process, an empty dictionary `{}` is returned.
    """
    logger.info(f"Reading URL: {url}")
    try:
        tweet_id = extract_tweet_id(url)
        guest_token = readGuestTokentxt()
        scrapedData = scrape_tweet(tweet_id, url, guest_token)
        return scrapedData
    except Exception as e:
        return {}
