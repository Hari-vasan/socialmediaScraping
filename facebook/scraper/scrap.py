import re
from utils.log import logger
from utils.helper import get_max_formatted_value


# Read the content of the file
def fetch_data(content, content_type):
    """
    The `fetch_data` function extracts play counts, likes count, share count, and comment count from
    content based on the specified content type.

    :param content: The `fetch_data` function you provided is designed to extract various counts (plays,
    likes, shares, comments) from a given content based on the content type. The function uses regular
    expressions to extract the counts from the content
    :param content_type: The `content_type` parameter in the `fetch_data` function is used to determine
    the type of content being processed. In this function, if the `content_type` is "Video", the
    function will extract play counts from the content. Otherwise, it will extract likes count, share
    count, and
    :return: The `fetch_data` function returns a dictionary containing the extracted data from the
    provided content based on the specified content type. The dictionary includes keys for "plays",
    "likes", "shares", and "comments", with corresponding counts extracted from the content.
    """
    like_pattern = r'"i18n_reaction_count":\s*"([\d.]+[kKmM]?)"'
    plays_pattern = r'"play_count_reduced":"(\d+\.?\d*[KM]?)","play_count":(\d+)'
    share_pattern = r'"i18n_share_count":\s*"([\d.]+[kKmM]?)"'
    comment_pattern = (
        r'"comment_rendering_instance":\{"comments":\{"total_count":(\d+)\}\}'
    )

    # Initialize variables
    plays_count = 0
    likes_count = 0
    share_count = 0
    comment_count = 0

    try:
        # Extract play counts if content_type is "Video"
        if content_type == "Video":
            plays_matches = re.findall(plays_pattern, content)
            if plays_matches:
                play_count_reduced, play_count = plays_matches[0]
                plays_count = play_count_reduced
                logger.info(f"Extracted play count: {plays_count}")
            else:
                logger.info("No play count found")

        # Extract likes count
        likes_matches = re.findall(like_pattern, content)
        if likes_matches:
            likes_count = likes_matches[0]
            logger.info(f"Extracted likes count: {likes_count}")
        else:
            logger.info("No likes count found")

        # Extract share count
        share_matches = re.findall(share_pattern, content)
        if share_matches:
            share_count = get_max_formatted_value(share_matches)
            logger.info(f"Extracted share count: {share_count}")
        else:
            logger.info("No share count found")

        # Extract comment count
        comment_matches = re.findall(comment_pattern, content)
        if comment_matches:
            comment_count = get_max_formatted_value(comment_matches)
            logger.info(f"Extracted comment count: {comment_count}")
        else:
            logger.info("No comment count found")

    except Exception as e:
        logger.error(f"Error while fetching data: {str(e)}")

    # Construct result dictionary
    scrap_content = {
        "plays": plays_count,
        "likes": likes_count,
        "shares": share_count,
        "comments": comment_count,
    }

    return scrap_content
