from typing import Any, Dict, List, Tuple

def get_traces_and_spans_from_payload(
    payload: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Separate traces and spans from payload.

    Traces are identified by not having a "type" field.
    Spans are identified by having a "type" field.

    Args:
        payload: List of dicts containing trace and span data

    Returns:
        Tuple of (traces, spans) where both are lists of dicts with null values removed
    """
    traces = [_remove_nulls(x) for x in payload if "type" not in x]
    spans = [_remove_nulls(x) for x in payload if "type" in x]
    return traces, spans

