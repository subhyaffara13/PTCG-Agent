from typing import Optional

def _get_regional_uplift_multiplier(
    model_info: ModelInfo, data_residency: Optional[str]
) -> float:
    """
    Resolve the per-model regional-processing uplift multiplier for a given
    data-residency region.

    OpenAI applies a flat percentage uplift (e.g. +10%) on all token costs for
    requests served from a regionalized hostname (eu./us.api.openai.com). The
    multiplier is stored on the model entry as
    ``regional_processing_uplift_multiplier_<region>`` (e.g. 1.10).

    Returns 1.0 (no uplift) when ``data_residency`` is ``None`` or when the
    model has no multiplier configured for the given region.
    """
    if data_residency is None:
        return 1.0
    residency = data_residency.lower()
    if residency not in _VALID_DATA_RESIDENCIES:
        return 1.0
    multiplier = model_info.get(f"regional_processing_uplift_multiplier_{residency}")
    if multiplier is None:
        return 1.0
    try:
        return float(cast(float, multiplier))
    except (TypeError, ValueError):
        verbose_logger.exception(
            "Invalid regional_processing_uplift_multiplier_%s for model; "
            "defaulting to 1.0",
            residency,
        )
        return 1.0

