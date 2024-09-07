import requests
from urllib.parse import quote
import json
from utils.log import logger
from utils.helper import datetimefix
from twitter.scraper.readGuestToken import writeGuestTokentxt
from twitter.scraper.getCokkies import get_guest_token
from utils.helper import get_max_formatted_value


def scrape_tweet(tweet_id: str, url: str, guest_token: str) -> dict:
    """
    The function `scrape_tweet` scrapes tweet data using the Twitter GraphQL API, handling
    authentication and returning specific counts and metadata.

    :param tweet_id: The `tweet_id` parameter in the `scrape_tweet` function is the ID of the tweet that
    you want to scrape using the Twitter GraphQL API. This ID uniquely identifies the tweet on Twitter
    :type tweet_id: str
    :param url: The `url` parameter in the `scrape_tweet` function is used to pass the URL of the tweet
    that needs to be scraped. This URL might be needed to obtain a guest token for making requests to
    the Twitter GraphQL API
    :type url: str
    :param guest_token: The `guest_token` parameter in the `scrape_tweet` function is used as a token
    for authentication when making requests to the Twitter GraphQL API. This token allows the function
    to access certain resources on behalf of a guest user without requiring them to log in. It is passed
    as a parameter to the
    :type guest_token: str
    :return: The function `scrape_tweet` is returning a dictionary containing various counts related to
    a tweet, such as views, bookmarks, favorites, quotes, replies, retweets, and the tweet's date.
    """
    # Define the URL and query parameters
    base_url = "https://api.x.com/graphql/sCU6ckfHY0CyJ4HFjPhjtg/TweetResultByRestId"
    variables = {
        "tweetId": tweet_id,
        "withCommunity": False,
        "includePromotedContent": False,
        "withVoice": False,
    }
    features = {
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_enhance_cards_enabled": False,
    }
    field_toggles = {
        "withArticleRichContentState": True,
        "withArticlePlainText": False,
        "withGrokAnalyze": False,
        "withDisallowedReplyControls": False,
    }

    # URL encode the parameters
    variables_encoded = quote(json.dumps(variables))
    features_encoded = quote(json.dumps(features))
    field_toggles_encoded = quote(json.dumps(field_toggles))

    # Build the request URL
    request_url = f"{base_url}?variables={variables_encoded}&features={features_encoded}&fieldToggles={field_toggles_encoded}"

    # Define the headers
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "x-guest-token": guest_token,
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
    }
    proxies = {
        "http": "http://103.221.253.145/",
        "http": "82.146.40.75",
    }
    # Make the request
    response = requests.get(request_url, headers=headers, proxies=proxies)
    status = response.status_code
    # Check if the request was successful
    if status == 200:
        data = response.json()
        tweet_result = data.get("data", {}).get("tweetResult", {}).get("result", {})

        # Extract the counts
        legacy_data = tweet_result.get("legacy", {})

        # Retrieve specific counts, with default values if they don't exist
        views_count = get_max_formatted_value(
            [data["data"]["tweetResult"]["result"]["views"]["count"]]
        )
        bookmark_count = get_max_formatted_value([legacy_data.get("bookmark_count", 0)])
        favorite_count = get_max_formatted_value([legacy_data.get("favorite_count", 0)])
        quote_count = get_max_formatted_value([legacy_data.get("quote_count", 0)])
        reply_count = get_max_formatted_value([legacy_data.get("reply_count", 0)])
        retweet_count = get_max_formatted_value([legacy_data.get("retweet_count", 0)])
        date = datetimefix(legacy_data.get("created_at", 0))

        # Return the counts in a dictionary
        return {
            "views": views_count,
            "bookmark": bookmark_count,
            "favorite": favorite_count,
            "quote": quote_count,
            "reply": reply_count,
            "retweet": retweet_count,
            "date": date,
        }

    elif status != 200:
        guest_token = get_guest_token(url)
        writeGuestTokentxt(guest_token)
        return scrape_tweet(tweet_id, url, guest_token)

    else:
        print(f"Failed to fetch data: {response.text}")
        return {response.text}
