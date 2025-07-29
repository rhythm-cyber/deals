import requests
from bs4 import BeautifulSoup
import os


def generate_affiliate_link(asin):
    tag = os.getenv("AFFILIATE_AMAZON")
    return f"https://www.amazon.in/dp/{asin}?tag={tag}"


def get_amazon_deals():
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    url = "https://www.amazon.in/deals"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    deals = []
    for link in soup.select("a[href*='/dp/']")[:10]:
        href = link.get("href")
        if "/dp/" in href:
            asin = href.split("/dp/")[1].split("/")[0]
            title = link.get_text(strip=True)
            deal = {
                "title": title or f"Product {asin}",
                "affiliate_link": generate_affiliate_link(asin),
            }
            deals.append(deal)
    return deals
