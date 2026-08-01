
def _normalize_operation_ids(paths: Dict[str, Dict]) -> None:
    """Make FastAPI-generated operation IDs stable for multi-method routes.

    FastAPI derives the default operation ID suffix from the first item in the
    route's methods set. For routes registered with several HTTP methods, that
    set iteration order can vary between processes, which makes the snapshot
    drift even when no routes changed.
    """
    for path_ops in paths.values():
        if not isinstance(path_ops, dict):
            continue

        methods = {method for method in path_ops if method in HTTP_METHOD_SUFFIXES}
        if not methods:
            continue

        for method, operation in path_ops.items():
            if method not in HTTP_METHOD_SUFFIXES or not isinstance(operation, dict):
                continue

            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str):
                continue

            for suffix in methods:
                suffix_token = f"_{suffix}"
                if operation_id.endswith(suffix_token):
                    operation["operationId"] = (
                        operation_id[: -len(suffix_token)] + f"_{method}"
                    )
                    break

