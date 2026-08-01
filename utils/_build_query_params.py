
def _build_query_params(
    query_param_names: list,
    kwargs: Dict[str, Any],
) -> Dict[str, str]:
    """Build query parameters from kwargs."""
    params = {}
    for param_name in query_param_names:
        value = kwargs.get(param_name)
        if value is not None:
            params[param_name] = str(value) if not isinstance(value, str) else value
    return params

