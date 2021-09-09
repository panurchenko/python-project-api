import requests
import urllib.parse
from bs4 import BeautifulSoup as bs


def get_amount(phrase):
    base_url = "https://fast-anime.ru/search/?search"
    param = {'': phrase}
    url = base_url + urllib.parse.urlencode(param)
    headers = headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0)"
    }
    respond = bs(requests.get(url, headers=headers).text, "html.parser")
    paragraph = respond.find_all('p', class_="title has-text-grey-dark")
    amount = 0
    for x in paragraph[0].text.split():
        try:
            amount = int(x)
        except:
            continue
    return amount
