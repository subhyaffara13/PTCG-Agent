from typing import Any

def resolve_oci_schema_anyof(obj: Any) -> Any:
    """Resolve Pydantic v2 ``Optional[T]`` → ``anyOf`` patterns.

    Pydantic v2 emits ``{"anyOf": [{"type": "T"}, {"type": "null"}]}`` for
    ``Optional[T]``.  OCI models don't understand ``anyOf``, so we pick the
    first non-null branch and merge top-level metadata into it.
    """
    if isinstance(obj, dict):
        if "anyOf" in obj and "type" not in obj:
            non_null = [
                t
                for t in obj["anyOf"]
                if not (isinstance(t, dict) and t.get("type") == "null")
            ]
            if non_null:
                resolved = {**obj, **non_null[0]}
                resolved.pop("anyOf", None)
                return resolve_oci_schema_anyof(resolved)
        return {k: resolve_oci_schema_anyof(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_oci_schema_anyof(item) for item in obj]
    return obj

