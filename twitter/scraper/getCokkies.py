import requests
import re


def get_guest_token(url):
    """
    The function `get_guest_token` sends a GET request to a specified URL with defined headers and
    proxies to retrieve a guest token value from the response text.

    :param url: The `get_guest_token` function you provided seems to be attempting to retrieve a guest
    token from a given URL using specified headers and proxies. However, there are a couple of issues in
    the code snippet you shared:
    :return: The function `get_guest_token(url)` is returning the value of the "gt" cookie extracted
    from the response text of the provided URL. If the regex pattern matches and finds the "gt" cookie
    value, it will return that value. Otherwise, it will return an empty list `[]`.
    """
    proxies = {
        "http": "http://103.221.253.145/",
        "http": "82.146.40.75",
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": 'personalization_id="v1_P3q3vM6BHMOfSFxRgrkV3w=="; guest_id_marketing=172527612237915458; guest_id_ads=172527612237915458; guest_id=172527612237915458; night_mode=2',
        "referer": "https://twitter.com/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers, proxies=proxies)
    res = response.text
    match = re.search(r'document\.cookie="gt=([^;]*)', res)
    if match:
        gt_value = match.group(1)
        return gt_value
    else:
        return []
