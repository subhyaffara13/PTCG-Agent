from typing import Any, Optional

def _video_output_cost_per_second(
    model_info: Mapping[str, Any],
    video_resolution: Optional[str],
) -> Optional[float]:
    """
    Per-second video output rate from model_info.

    If ``video_resolution`` is set (e.g. ``1080p``, ``720p``, ``4k``), looks up
    ``output_cost_per_second_<resolution>`` first (e.g. ``output_cost_per_second_1080p``),
    then falls back to ``output_cost_per_second``.
    """
    r = (video_resolution or "").strip().lower()
    if r:
        suffix = _video_resolution_to_cost_field_suffix(r)
        if suffix is not None:
            tier_key = f"output_cost_per_second_{suffix}"
            tier_rate = model_info.get(tier_key)
            if tier_rate is not None:
                return float(tier_rate)
    out = model_info.get("output_cost_per_second")
    if out is not None:
        return float(out)
    return None

