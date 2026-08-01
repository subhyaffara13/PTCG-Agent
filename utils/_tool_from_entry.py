
def _tool_from_entry(entry: object) -> ToolDefinition | None:
    """One ``tools``/``functions`` entry → ``ToolDefinition``, or ``None`` if unusable."""
    if not isinstance(entry, dict):
        return None
    fn = entry.get("function") if "function" in entry else entry
    if not isinstance(fn, dict):
        return None
    name = as_str(fn.get("name"))
    if not name:
        return None
    params = fn.get("parameters")
    parameters_json: str | None = None
    if params is not None:
        try:
            parameters_json = json.dumps(params, default=str)
        except Exception:
            parameters_json = None
    return ToolDefinition(
        name=name,
        description=as_str(fn.get("description")),
        parameters_json=parameters_json,
    )

