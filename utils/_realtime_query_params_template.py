from typing import List, Optional, Tuple

def _realtime_query_params_template(
    model: Optional[str], intent: Optional[str]
) -> Tuple[Tuple[str, str], ...]:
    """
    Build a hashable representation of the realtime query params so we can cache
    the repetitive model/intent combinations.
    """
    params: List[Tuple[str, str]] = []
    if model is not None:
        params.append(("model", model))
    if intent is not None:
        params.append(("intent", intent))
    return tuple(params)

