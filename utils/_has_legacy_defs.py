
def _has_legacy_defs(schema: object) -> bool:
    if not isinstance(schema, dict):
        return False
    components = schema.get("components")
    return "definitions" in schema or (
        isinstance(components, dict) and isinstance(components.get("schemas"), dict)
    )

