
def _resolve_param_list(
    raw: List[Dict[str, Any]], component_params: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Resolve $refs in a parameter list, dropping any unresolvable entries."""
    result = []
    for p in raw:
        resolved = _resolve_ref(p, component_params)
        if resolved is not None and resolved.get("name"):
            result.append(resolved)
    return result

