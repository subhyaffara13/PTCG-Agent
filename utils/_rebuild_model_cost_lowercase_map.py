from typing import Dict

def _rebuild_model_cost_lowercase_map() -> Dict[str, str]:
    """Rebuild the case-insensitive lookup map from the current model_cost.

    Returns:
        The rebuilt map (guaranteed to be not None).
    """
    global _model_cost_lowercase_map
    _model_cost_lowercase_map = {k.lower(): k for k in litellm.model_cost}
    return _model_cost_lowercase_map

