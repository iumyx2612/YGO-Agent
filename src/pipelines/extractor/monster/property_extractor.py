from typing import Callable, Tuple, Dict, List, Any
from typing_extensions import Self

from llama_index.core.output_parsers.utils import parse_json_markdown
from llama_index.core.graph_stores.types import (
    EntityNode,
    KG_NODES_KEY,
    KG_RELATIONS_KEY,
    Relation,
)

from src.modules.common.extractor.graphrag_extractor import GraphRAGExtractor
from src.modules.schema.card import CardNode
from src.pipelines.card.monster.card_property import MonsterPropertiesPipeline


def parse_monster_property(string: str) -> Tuple[str, List[Dict], List[Dict]]:
    entity_dict = parse_json_markdown(string)

    card_type = entity_dict["card_type"]
    entities = entity_dict["entities"]

    relations = []
    for entity in entities:
        relations.append(
            {
                "target_entity": entity["entity_name"],
                "label": "Is"
            }
        )

    return card_type, entities, relations


class MonsterPropertyExtractor(GraphRAGExtractor):

    @classmethod
    def from_defaults(
            cls,
            extraction_pipeline: MonsterPropertiesPipeline,
            parse_fn: Callable = parse_monster_property,
            num_workers: int = 4,
            **kwargs
    ) -> Self:
        return cls(extraction_pipeline, parse_fn, num_workers, **kwargs)

    def _collect_entities(self, entities: List[Dict]) -> List[EntityNode]:
        results = []

        for entity in entities:
            entity_name = entity["entity_name"]
            results.append(
                EntityNode(
                    name=entity_name
                )
            )

        return results

    def _collect_relations(self,
                           node: CardNode,
                           relations: List[Dict],
                           entity_nodes: List[EntityNode]) -> List[Relation]:
        results = []

        for target_node, relation in zip(entity_nodes, relations):
            source_node = node
            relation_node = Relation(
                label=relation["label"],
                source_id=source_node.id,
                target_id=target_node.id
            )
            results.append(relation_node)

        return results

    async def _aextract(self, node: CardNode, **kwargs) -> CardNode:
        """Extract triples from a node."""

        try:
            llm_response = await self.extraction_pipeline.aanalyze_card(
                node.info,
                **kwargs
            )
            card_type, entities, entities_relationship = self.parse_fn(llm_response)
        except ValueError:
            entities = []
            entities_relationship = []
            card_type = "Effect Monster"

        existing_nodes = node.metadata.pop(KG_NODES_KEY, [])
        existing_relations = node.metadata.pop(KG_RELATIONS_KEY, [])

        entity_nodes = self._collect_entities(entities)
        existing_nodes.extend(entity_nodes)
        existing_relations.extend(
            self._collect_relations(node, entities_relationship, entity_nodes)
        )

        node.label = card_type
        node.metadata[KG_NODES_KEY] = existing_nodes
        node.metadata[KG_RELATIONS_KEY] = existing_relations
        return node