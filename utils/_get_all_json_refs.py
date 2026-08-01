
def _get_all_json_refs(item: Any) -> set[JsonRef]:
    """Get all the definitions references from a JSON schema."""
    refs: set[JsonRef] = set()
    stack = [item]

    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for key, value in current.items():
                if key == 'examples' and isinstance(value, list):
                    # Skip examples that may contain arbitrary values and references
                    # (e.g. `{"examples": [{"$ref": "..."}]}`). Note: checking for value
                    # of type list is necessary to avoid skipping valid portions of the schema,
                    # for instance when "examples" is used as a property key. A more robust solution
                    # could be found, but would require more advanced JSON Schema parsing logic.
                    continue
                if key == '$ref' and isinstance(value, str):
                    refs.add(JsonRef(value))
                elif isinstance(value, dict):
                    stack.append(value)
                elif isinstance(value, list):
                    stack.extend(value)
        elif isinstance(current, list):
            stack.extend(current)

    return refs

