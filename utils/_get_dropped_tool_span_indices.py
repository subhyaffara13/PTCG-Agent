from typing import List, Set

def _get_dropped_tool_span_indices(
    kept_indices: Set[int], tool_exchange_spans: List[Set[int]]
) -> Set[int]:
    dropped_tool_span_indices: Set[int] = set()
    for span in tool_exchange_spans:
        if not any(idx in kept_indices for idx in span):
            dropped_tool_span_indices.update(span)
    return dropped_tool_span_indices

