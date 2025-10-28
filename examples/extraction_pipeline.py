from dotenv import load_dotenv
import json

from llama_index.llms.azure_openai import AzureOpenAI

from src.modules.schema.card import CardInfo, CardNode
from src.pipelines.card.monster.card_property import (
    MonsterPropertiesPipeline
)
from src.pipelines.extractor.monster.property_extractor import MonsterPropertyExtractor


load_dotenv()
llm = AzureOpenAI(
    model="gpt-4.1-mini",
    engine="gpt-4.1-mini",
    temperature=0,
    max_retries=1
)


pipe = MonsterPropertiesPipeline.from_defaults(llm)
extractor = MonsterPropertyExtractor.from_defaults(pipe)
path = "raw_data/Maliss Dormouse.json"
card_data = json.load(open(path, encoding="utf-8"))
card_info = CardInfo.from_dict(card_data)

card_node = CardNode(
    name=card_info.name,
    info=card_info
)

node = extractor([card_node])