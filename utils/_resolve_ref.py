from typing import Any, Dict, Optional

def _resolve_ref(
    param: Dict[str, Any], component_params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Resolve a single parameter, following a $ref if present.

    Returns the resolved param dict, or None if the $ref target is absent from
    components (so callers can skip/filter it rather than propagating a stub
    with name=None that would corrupt deduplication).
    """
    ref = param.get("$ref", "")
    if not ref.startswith("#/components/parameters/"):
        return param
    return component_params.get(ref.split("/")[-1])

