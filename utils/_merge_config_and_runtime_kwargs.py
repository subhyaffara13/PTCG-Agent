from typing import Any

def _merge_config_and_runtime_kwargs(
    config_params: dict[str, Any],
    runtime_kwargs: dict[str, Any],
) -> dict[str, Any]:
    """Merge config parameters with runtime kwargs. Config params take precedence,
    since they represent the values being autotuned.

    Args:
        config_params: Parameters from CustomOpConfig (autotuning knobs)
        runtime_kwargs: Runtime non-tensor kwargs from _extract_tensor_inputs

    Returns:
        Merged kwargs dictionary with config values taking precedence
    """
    merged_kwargs = runtime_kwargs.copy()
    merged_kwargs.update(config_params)
    return merged_kwargs

