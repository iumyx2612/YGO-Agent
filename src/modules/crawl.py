from typing import List

import requests
import aiohttp
import json
import logging

from src.modules.schema.card import CardRequest, CardInfo

BASE_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
PARAMETER_STRING = "?"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This ensures output to terminal
    ]
)

logger = logging.getLogger(__name__)


async def acrawl(
        card_request: CardRequest
) -> List[CardInfo]:
    url = ""

    request_dict = card_request.dict()
    for param, value in request_dict.items():
        if value is not None:
            url += f"{param}={value}&"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{BASE_URL}{PARAMETER_STRING}{url}"
            ) as response:
                response.raise_for_status()

                data = await response.json()
                print(data)
    except Exception as e:
        print(e)
        pass


def crawl(
        card_request: CardRequest
) -> List[CardInfo]:
    url = ""

    request_dict = card_request.dict()
    for param, value in request_dict.items():
        if value is not None:
            url += f"{param}={value}&"
    results = requests.post(f"{BASE_URL}{PARAMETER_STRING}{url}").text
    try:
        results = json.loads(results)["data"]
        infos = []
        for result in results:
            info = CardInfo.from_dict(result)
            infos.append(info)
        return infos
    except KeyError:
        logger.error(f"Can't not crawl card with info {card_request.dict()}")
        pass