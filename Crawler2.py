"""
Simple web crawler.
Displays all the links in the webpage and their links.
This method could be used to find all webpages or files in a website.
"""
import requests
import re
import urllib.parse as urlparse

global links
links = []

# Extract links from url
def extract_links_from(url):
    response = requests.get(url)
    return re.findall(b'(?:href=")(.*?)"',response.content)

# Perform crawling
def crawl(target_url):
    href_links = extract_links_from(target_url)
    for link in href_links:
        link = urlparse.urljoin(target_url,link.decode())
        links.append(link)
        if "#" in link and link not in links:
            links.append(link)
            print(link)
            crawl(link)

def PerformCrawl(url):
    crawl(str(url))
    global links
    print(links)
    return links
