from typing import List
import json
import os

from src.modules.crawl import crawl
from src.modules.schema.card import CardInfo, CardRequest


class CrawlPipeline:
    def crawl_from_json_file(self, file_path: str) -> List[CardInfo]:
        requests = json.load(open(file_path, 'r'))

        results = []
        for req in requests:
            request = CardRequest.from_dict(req)
            result = crawl(request)
            results.extend(result)

        return results

    def save_crawl_data(
            self,
            card_infos: List[CardInfo],
            save_folder: str
    ):
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for card_info in card_infos:
            name = card_info.name

            with open(f"{save_folder}/{name}.json", 'w', encoding="utf-8") as f:
                f.write(card_info.model_dump_json(indent=4))