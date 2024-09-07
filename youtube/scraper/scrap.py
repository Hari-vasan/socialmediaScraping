import instaloader
from utils.log import logger
from utils.helper import get_max_formatted_value, datetimefix
from bs4 import BeautifulSoup
import requests
import re


# Read the content of the file
def fetch_data(url):
    """
    The function `fetch_data` fetches data from a given URL, extracts views, likes, comments, and date
    information, and returns a dictionary with this information.

    :param url: The `fetch_data` function you provided seems to be designed to fetch data from a given
    URL, extract specific information like views, likes, comments, and date, and return it in a
    dictionary format
    :return: The `fetch_data` function returns a dictionary containing the following keys and their
    corresponding values:
    - "views": views_count
    - "likes": likes_count
    - "comments": comment_count
    - "date": date_str
    """

    try:
        # getting the request from url
        response = requests.get(url)

        soup = BeautifulSoup(requests.get(url).text, "lxml")
        content = response.text
        likes_pattern = r'"likeButtonViewModel":\{"likeButtonViewModel":\{"toggleButtonViewModel":\{"toggleButtonViewModel":\{"defaultButtonViewModel":\{"buttonViewModel":\{"iconName":"LIKE","title":"(\d+\.?\d*[KM]?)"'
        comment_pattern = r'"commentCount":\{"simpleText":"(\d+)"\}'
        date_pattern = r'itemprop="datePublished" content="([^"]+)"'

        views_count = get_max_formatted_value(
            [soup.select_one('meta[itemprop="interactionCount"][content]')["content"]]
        )
        likes_count = get_max_formatted_value(re.findall(likes_pattern, content))
        comment_count = get_max_formatted_value(re.findall(comment_pattern, content))
        date = re.findall(date_pattern, content)
        date_str = date[0]
    except Exception as e:
        logger.error(f"Error while fetching data: {str(e)}")

    # Construct result dictionary
    scrap_content = {
        "views": views_count,
        "likes": likes_count,
        "comments": comment_count,
        "date": date_str,
    }

    return scrap_content
