
def _strip_operation_id_method_suffix(operation_id: str) -> str:
    base, separator, suffix = operation_id.rpartition("_")
    if separator and suffix in _OPENAPI_HTTP_METHODS:
        return base
    return operation_id

