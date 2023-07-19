#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    Obtain the HTML content of a particular URL and return it """

import redis
import requests

r = redis.Redis()

def get_page(url: str) -> str:
    """ Track how many times a particular URL was accessed in the key
        "count:{url}" and cache the result with an expiration time of 10 seconds """
    count_key = f"count:{url}"
    cached_key = f"cached:{url}"

    r.incr(count_key)  # Increment the count for the URL
    cached_html = r.get(cached_key)  # Check if the URL is already cached

    if cached_html is not None:
        return cached_html.decode("utf-8")  # Return the cached HTML content

    resp = requests.get(url)
    html_content = resp.text

    r.setex(cached_key, 10, html_content)  # Cache the HTML content with an expiration time of 10 seconds

    return html_content


if __name__ == "__main__":
    page_content = get_page('http://slowwly.robertomurray.co.uk')
    print(page_content)
