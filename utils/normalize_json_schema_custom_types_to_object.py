
def normalize_json_schema_custom_types_to_object(schema: dict) -> None:
    """
    In-place: replace JSON Schema ``type: \"custom\"`` with ``\"object\"`` (iterative walk).

    Anthropic / Claude Code use ``custom`` for tool schemas; Bedrock Invoke and
    Bedrock Converse only accept standard JSON Schema type strings.

    Uses an explicit stack (not recursion) to satisfy recursive-function guards in CI.
    """
    stack: List[Any] = [schema]
    seen: set[int] = set()
    while stack:
        node = stack.pop()
        if not isinstance(node, dict):
            continue
        node_id = id(node)
        if node_id in seen:
            continue
        seen.add(node_id)
        if node.get("type") == "custom":
            node["type"] = "object"
        items = node.get("items")
        if isinstance(items, dict):
            stack.append(items)
        addl = node.get("additionalProperties")
        if isinstance(addl, dict):
            stack.append(addl)
        props = node.get("properties")
        if isinstance(props, dict):
            for sub in props.values():
                if isinstance(sub, dict):
                    stack.append(sub)
        for combiner in ("allOf", "anyOf", "oneOf"):
            arr = node.get(combiner)
            if isinstance(arr, list):
                for sub in arr:
                    if isinstance(sub, dict):
                        stack.append(sub)

