
def _canonical_path(route: str) -> str:
    """
    Normalise a passthrough route to a bare /v1/... path for map lookup.

    Examples:
      /openai_passthrough/v1/files   -> /v1/files
      /openai/v1/files               -> /v1/files
      /azure/openai/files            -> /v1/files   (Azure omits /v1/)
      /azure/openai/batches/batch_x  -> /v1/batches/batch_x
    """
    stripped = _PASSTHROUGH_PREFIX_RE.sub("", route) or "/"
    # Azure API paths don't include /v1/ — add it so they match the map keys.
    if not stripped.startswith("/v1/") and stripped != "/":
        stripped = "/v1" + stripped
    return stripped

