
def _set_nested_metadata_value(
    metadata: Dict[str, Any], key_path: str, value: Any
) -> None:
    placeholder = "\x00"
    parts = key_path.replace("\\.", placeholder).split(".")
    parts = [p.replace(placeholder, ".") for p in parts]
    current: Any = metadata
    for part in parts[:-1]:
        existing = current.get(part)
        if not isinstance(existing, dict):
            existing = {}
            current[part] = existing
        current = existing
    current[parts[-1]] = value

