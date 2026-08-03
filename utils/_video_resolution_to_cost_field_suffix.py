from typing import Optional

def _video_resolution_to_cost_field_suffix(resolution: str) -> Optional[str]:
    """
    Map usage resolution to a safe suffix for ``output_cost_per_second_<suffix>`` keys.

    Note: Currently only ``output_cost_per_second_1080p`` is explicitly declared in
    ModelInfo (types/utils.py). Other resolution tiers (e.g., 720p, 4k) can be added
    to model_prices_and_context_window.json but are not exposed via get_model_info()
    until added to the ModelInfo TypedDict.
    """
    r = resolution.strip().lower()
    if not r:
        return None
    safe = "".join(c for c in r if c.isalnum() or c == "_")
    if not safe or len(safe) > 24:
        return None
    return safe

