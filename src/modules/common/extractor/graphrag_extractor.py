import asyncio
from abc import abstractmethod
from typing import Any, List, Callable, Union
from typing_extensions import Self

from llama_index.core.async_utils import run_jobs
from llama_index.core.indices.property_graph.utils import (
    default_parse_triplets_fn,
)
from llama_index.core.graph_stores.types import (
    EntityNode,
    KG_NODES_KEY,
    KG_RELATIONS_KEY,
    Relation,
)
from llama_index.core.llms.llm import LLM
from llama_index.core.prompts import PromptTemplate
from llama_index.core.schema import TransformComponent

from src.modules.schema.card import CardNode
from src.pipelines.card.base_card import BaseCardPipeline


class GraphRAGExtractor(TransformComponent):
    """Extract triples from a graph.

    Uses an LLM and a simple prompt + output parsing to extract paths (i.e. triples) and entity, relation descriptions from text.

    Args:
        llm (LLM):
            The language model to use.
        extract_prompt (Union[str, PromptTemplate]):
            The prompt to use for extracting triples.
        parse_fn (callable):
            A function to parse the output of the language model.
        num_workers (int):
            The number of workers to use for parallel processing.
        max_paths_per_chunk (int):
            The maximum number of paths to extract per chunk.
    """

    extraction_pipeline: BaseCardPipeline
    parse_fn: Callable
    num_workers: int

    def __init__(
        self,
        extraction_pipeline: BaseCardPipeline,
        parse_fn: Callable = default_parse_triplets_fn,
        num_workers: int = 4,
        **kwargs
    ) -> None:
        """Init params."""

        super().__init__(
            extraction_pipeline=extraction_pipeline,
            parse_fn=parse_fn,
            num_workers=num_workers
        )

    @classmethod
    def class_name(cls) -> str:
        return "GraphExtractor"

    @classmethod
    def from_defaults(
            cls,
            extraction_pipeline: BaseCardPipeline,
            parse_fn: Callable = default_parse_triplets_fn,
            num_workers: int = 4,
            **kwargs
    ) -> Self:
        return cls(extraction_pipeline, parse_fn, num_workers, **kwargs)

    def __call__(
        self, nodes: List[CardNode], show_progress: bool = False, **kwargs: Any
    ) -> List[CardNode]:
        """Extract triples from nodes."""
        return asyncio.run(
            self.acall(nodes, show_progress=show_progress, **kwargs)
        )

    @abstractmethod
    def _collect_entities(self, entities: Any) -> List[EntityNode]:
        ...

    @abstractmethod
    def _collect_relations(self, relations: Any, entity_nodes: List[EntityNode]) -> List[Relation]:
        ...

    async def _aextract(self, node: CardNode, **kwargs) -> CardNode:
        """Extract triples from a node."""

        try:
            llm_response = await self.extraction_pipeline.aanalyze_card(
                node.info,
                **kwargs
            )
            entities, entities_relationship = self.parse_fn(llm_response)
        except ValueError:
            entities = []
            entities_relationship = []

        existing_nodes = node.metadata.pop(KG_NODES_KEY, [])
        existing_relations = node.metadata.pop(KG_RELATIONS_KEY, [])

        entity_nodes = self._collect_entities(entities)
        existing_nodes.extend(entity_nodes)
        existing_relations.extend(
            self._collect_relations(entities_relationship, entity_nodes)
        )

        node.metadata[KG_NODES_KEY] = existing_nodes
        node.metadata[KG_RELATIONS_KEY] = existing_relations
        return node

    async def acall(
        self, nodes: List[CardNode], show_progress: bool = False, **kwargs: Any
    ) -> List[CardNode]:
        """Extract triples from nodes async."""
        jobs = []
        for node in nodes:
            jobs.append(self._aextract(node, **kwargs))

        return await run_jobs(
            jobs,
            workers=self.num_workers,
            show_progress=show_progress,
            desc="Extracting paths from text",
        )