
def resolve_oci_schema_refs(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Inline all ``$ref``/``$defs`` references — OCI does not support JSON Schema ``$ref``."""
    defs = schema.get("$defs", {})
    resolving_stack: set = set()

    def _resolve(obj: Any) -> Any:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref = obj["$ref"]
                if ref.startswith("#/$defs/"):
                    key = ref.split("/")[-1]
                    if key in resolving_stack:
                        return {"type": "object"}  # break cycles
                    resolving_stack.add(key)
                    try:
                        return _resolve(defs.get(key, obj))
                    finally:
                        resolving_stack.discard(key)
                return obj  # external $ref — leave unchanged
            return {k: _resolve(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_resolve(item) for item in obj]
        return obj

    resolved = _resolve(schema)
    if isinstance(resolved, dict):
        resolved.pop("$defs", None)
    return resolved

