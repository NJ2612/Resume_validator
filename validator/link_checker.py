import requests
import time
from config import REQUEST_TIMEOUT, REQUEST_DELAY, USER_AGENT


CACHE = {}


def check_link(url):

    if url in CACHE:
        return CACHE[url]

    if not url:
        return False

    if "localhost" in url or "127.0.0.1" in url:
        CACHE[url] = False
        return False

    try:
        headers = {"User-Agent": USER_AGENT}

        response = requests.head(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )

        status = response.status_code < 400

        CACHE[url] = status

        time.sleep(REQUEST_DELAY)

        return status

    except:
        CACHE[url] = False
        return False