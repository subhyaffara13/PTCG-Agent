import copy
from typing import Any, Callable

def get_embedding_qat_module_mappings() -> dict[Callable, Any]:
    """Get module mapping for quantization aware training
    This is includes default values in addition to
    enabling qat for embeddings.
    """
    mapping = copy.deepcopy(DEFAULT_QAT_MODULE_MAPPINGS)
    mapping[nn.EmbeddingBag] = nnqat.EmbeddingBag
    mapping[nn.Embedding] = nnqat.Embedding
    return mapping

