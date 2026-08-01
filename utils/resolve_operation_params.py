
def resolve_operation_params(
    operation: Dict[str, Any],
    path_item: Dict[str, Any],
    components: Dict[str, Any],
) -> Dict[str, Any]:
    """Return a copy of *operation* with fully-resolved, merged parameters.

    Handles two common patterns in real-world OpenAPI specs:

    1. **$ref parameters** — ``{"$ref": "#/components/parameters/per-page"}``
       instead of inline objects.  Each ref is resolved against
       ``components["parameters"]``; unresolvable refs are silently dropped so
       they cannot corrupt the deduplication set with ``(None, None)`` keys.

    2. **Path-level parameters** — params defined on the path item that apply
       to every HTTP method on that path (e.g. ``owner``, ``repo``).  They are
       merged with the operation-level params; operation-level wins when the
       same ``name`` + ``in`` combination appears in both.
    """
    component_params = components.get("parameters", {})
    path_level = _resolve_param_list(path_item.get("parameters", []), component_params)
    op_level = _resolve_param_list(operation.get("parameters", []), component_params)
    op_keys = {(p["name"], p.get("in")) for p in op_level}
    merged = [
        p for p in path_level if (p["name"], p.get("in")) not in op_keys
    ] + op_level
    result = dict(operation)
    result["parameters"] = merged
    return result

