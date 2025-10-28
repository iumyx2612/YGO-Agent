from dotenv import load_dotenv
import os
import json
from tqdm import tqdm

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.graph_stores import SimplePropertyGraphStore
from llama_index.core.graph_stores.types import (
    KG_NODES_KEY,
    KG_RELATIONS_KEY,)

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
graph_store = SimplePropertyGraphStore()

path = "raw_data/Maliss Dormouse.json"
card_data = json.load(open(path, encoding="utf-8"))
card_info = CardInfo.from_dict(card_data)

card_node = CardNode(
    name=card_info.name,
    info=card_info
)

node = extractor([card_node])[0]
nodes = [node]
entity_nodes = node.metadata[KG_NODES_KEY]
existing_relations = node.metadata[KG_RELATIONS_KEY]
nodes.extend(entity_nodes)

graph_store.upsert_nodes(nodes)
graph_store.upsert_relations(existing_relations)

graph_store.persist("db/Maliss_archetype.json")
graph_store.save_networkx_graph() # Visualize