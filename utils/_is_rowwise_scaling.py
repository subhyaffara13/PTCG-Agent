from typing import Any

def _is_rowwise_scaling(sz: Any, transpose: bool) -> bool:
    idx = 0 if transpose else -1
    return V.graph.sizevars.statically_known_equals(sz[idx], 1)

