import re


def extract_tweet_id(url: str) -> str:
    """
    The function `extract_tweet_id` extracts the tweet ID from a given tweet URL using regular
    expressions in Python.

    :param url: https://twitter.com/Twitter/status/1234567890123456789
    :type url: str
    :return: The function `extract_tweet_id` returns the tweet ID extracted from the given URL. If a
    match is found using the regular expression pattern "status/(\d+)", it returns the tweet ID. If no
    match is found, it raises a ValueError with the message "Invalid URL or tweet ID not found."
    """
    """
    Extract tweet ID from a given URL.

    Args:
    - url: The URL of the tweet.

    Returns:
    - The tweet ID.
    """
    match = re.search(r"status/(\d+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid URL or tweet ID not found.")
