
def ensure_unique_openapi_operation_ids(
    openapi_schema: Dict[str, Any],
    reserved_operation_ids: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    operation_entries = []
    operation_id_counts: Dict[str, int] = {}
    for path_item in openapi_schema.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method not in _OPENAPI_HTTP_METHODS or not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str):
                continue
            operation_entries.append((method, operation, operation_id))
            operation_id_counts[operation_id] = (
                operation_id_counts.get(operation_id, 0) + 1
            )

    used_operation_ids = set(reserved_operation_ids or set())
    seen_operation_ids: Set[str] = set()
    for method, operation, operation_id in operation_entries:
        should_rewrite = (
            operation_id_counts[operation_id] > 1
            or operation_id in used_operation_ids
            or operation_id in seen_operation_ids
        )
        if not should_rewrite:
            seen_operation_ids.add(operation_id)
            used_operation_ids.add(operation_id)
            continue

        base_operation_id = _strip_operation_id_method_suffix(operation_id)
        new_operation_id = f"{base_operation_id}_{method}"
        suffix = 2
        while (
            new_operation_id in used_operation_ids
            or new_operation_id in seen_operation_ids
        ):
            new_operation_id = f"{base_operation_id}_{method}_{suffix}"
            suffix += 1
        operation["operationId"] = new_operation_id
        seen_operation_ids.add(new_operation_id)
        used_operation_ids.add(new_operation_id)

    if reserved_operation_ids is not None:
        reserved_operation_ids.update(used_operation_ids)

    return openapi_schema

