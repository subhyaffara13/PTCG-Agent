
def _append_payload_to_scan_stack(
    payload_stack: list[tuple[Any, int]],
    value: Any,
    next_depth: int,
) -> None:
    if isinstance(value, dict):
        if next_depth > DEFAULT_MAX_RECURSE_DEPTH:
            _raise_vector_store_scan_depth_exceeded()
        payload_stack.append((value, next_depth))
    elif isinstance(value, list):
        if next_depth > DEFAULT_MAX_RECURSE_DEPTH:
            if any(isinstance(item, (dict, list)) for item in value):
                _raise_vector_store_scan_depth_exceeded()
            return
        payload_stack.append((value, next_depth))

