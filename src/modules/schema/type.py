from typing import Any, Dict, Optional
from typing_extensions import Self
import json

from llama_index.core.graph_stores.types import EntityNode as LEntityNode
from llama_index.core.bridge.pydantic import BaseModel


class BaseComponent(BaseModel):

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        return self.model_dump(**kwargs)

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        data = self.dict(**kwargs)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        data = dict(data)
        if isinstance(kwargs, dict):
            data.update(kwargs)
        return cls(**data)

    @classmethod
    def from_json(cls, data_str: str, **kwargs: Any) -> Self:  # type: ignore
        data = json.loads(data_str)
        return cls.from_dict(data, **kwargs)


class EntityNode(LEntityNode):

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs: Any) -> Self:  # type: ignore
        data = dict(data)
        if isinstance(kwargs, dict):
            data.update(kwargs)
        return cls(**data)

    @classmethod
    def from_json(cls, data_str: str, **kwargs: Any) -> Self:  # type: ignore
        data = json.loads(data_str)
        return cls.from_dict(data, **kwargs)