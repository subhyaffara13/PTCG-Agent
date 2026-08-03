from typing import Any, Dict, List, Optional

def random_greedy(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    idx_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
    **optimizer_kwargs: Any,
) -> ArrayType:
    """A simple wrapper around the `RandomGreedy` optimizer."""
    optimizer = RandomGreedy(**optimizer_kwargs)
    return optimizer(inputs, output, idx_dict, memory_limit)

