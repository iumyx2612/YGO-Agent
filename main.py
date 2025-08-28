import requests
import json
from pprint import pprint
from enum import Enum, auto

from src.crawl.model import CardInfo


url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
data = requests.post(
    f"{url}?archetype=Maliss"
).text

data = json.loads(data)["data"][0]

info = CardInfo.from_dict(data)
print(info)