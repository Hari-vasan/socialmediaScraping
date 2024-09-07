import instaloader
from utils.log import logger
from utils.helper import get_max_formatted_value


# Read the content of the file
def fetch_data(url):
    """
    The function `fetch_data` fetches data such as likes, comments, and date from a given Instagram post
    URL.

    :param url: The `fetch_data` function you provided seems to be fetching data from an Instagram post
    using Instaloader library based on the given URL. It extracts information like likes count, comments
    count, and date of the post
    :return: The `fetch_data` function returns a dictionary containing the number of likes, number of
    comments, and the date of a post fetched from a given URL.
    """

    try:
        L = instaloader.Instaloader()
        if "reels" in url:
            split_by = "reels/"
        else:
            split_by = "p/"
        post = instaloader.Post.from_shortcode(
            L.context, url.split(split_by)[1].strip("/ ")
        )

        likes_count = get_max_formatted_value([post.likes])
        comment_count = get_max_formatted_value([post.comments])
        date = post.date_utc
        date_str = date.isoformat()
    except Exception as e:
        logger.error(f"Error while fetching data: {str(e)}")

    # Construct result dictionary
    scrap_content = {
        "likes": likes_count,
        "comments": comment_count,
        "date": date_str,
    }

    return scrap_content
