
def parse_admin_env_vars(
    env_vars: Optional[Iterable[Any]],
) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
    """Split admin-configured env var entries into globals and per-user specs.

    Accepts the raw value of ``MCPServer.env_vars`` (list of dicts or Pydantic
    models). Returns:

    - ``global_values``: ``{name: value}`` for entries with ``scope=="global"``.
    - ``user_specs``: list of ``{name, description}`` for entries with
      ``scope=="user"`` — these are the names the user must fill in.

    Unknown / malformed entries are skipped silently.
    """
    global_values: Dict[str, str] = {}
    user_specs: List[Dict[str, Any]] = []
    if not env_vars:
        return global_values, user_specs
    for raw in env_vars:
        if raw is None:
            continue
        if hasattr(raw, "model_dump"):
            entry = raw.model_dump()
        elif isinstance(raw, dict):
            entry = raw
        else:
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            continue
        scope = entry.get("scope") or "global"
        if scope == "user":
            user_specs.append({"name": name, "description": entry.get("description")})
        else:
            value = entry.get("value")
            global_values[name] = "" if value is None else str(value)
    return global_values, user_specs

