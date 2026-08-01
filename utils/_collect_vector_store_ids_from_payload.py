
def _collect_vector_store_ids_from_payload(payload: Any) -> set[str]:
    vector_store_ids: set[str] = set()
    payload_stack = [(payload, 0)]

    while payload_stack:
        current_payload, depth = payload_stack.pop()
        if depth > DEFAULT_MAX_RECURSE_DEPTH:
            _raise_vector_store_scan_depth_exceeded()

        if isinstance(current_payload, dict):
            for key, value in current_payload.items():
                if key == "vector_store_id":
                    if not isinstance(value, str) or not value:
                        raise HTTPException(
                            status_code=400,
                            detail={
                                "error": "vector_store_id must be a non-empty string"
                            },
                        )
                    vector_store_ids.add(value)
                    continue
                if isinstance(value, (dict, list)):
                    _append_payload_to_scan_stack(
                        payload_stack=payload_stack,
                        value=value,
                        next_depth=depth + 1,
                    )
        elif isinstance(current_payload, list):
            for item in current_payload:
                _append_payload_to_scan_stack(
                    payload_stack=payload_stack,
                    value=item,
                    next_depth=depth + 1,
                )

    return vector_store_ids

