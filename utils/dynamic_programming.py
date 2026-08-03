from typing import Any, Dict, List, Optional

def dynamic_programming(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
    **kwargs: Any,
) -> PathType:
    optimizer = DynamicProgramming(**kwargs)
    return optimizer(inputs, output, size_dict, memory_limit)

