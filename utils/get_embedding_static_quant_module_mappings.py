import copy
from typing import Any, Callable

def get_embedding_static_quant_module_mappings() -> dict[Callable, Any]:
    """Get module mapping, including mapping for embedding QAT"""
    mapping = copy.deepcopy(DEFAULT_STATIC_QUANT_MODULE_MAPPINGS)
    mapping[nnqat.EmbeddingBag] = nnq.EmbeddingBag
    mapping[nnqat.Embedding] = nnq.Embedding
    return mapping

