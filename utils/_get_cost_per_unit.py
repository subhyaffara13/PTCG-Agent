from typing import Optional

def _get_cost_per_unit(
    model_info: ModelInfo, cost_key: str, default_value: Optional[float] = 0.0
) -> Optional[float]:
    # Sometimes the cost per unit is a string (e.g.: If a value like "3e-7" was read from the config.yaml)
    cost_per_unit = model_info.get(cost_key)
    if isinstance(cost_per_unit, float):
        return cost_per_unit
    if isinstance(cost_per_unit, int):
        return float(cost_per_unit)
    if isinstance(cost_per_unit, str):
        try:
            return float(cost_per_unit)
        except ValueError:
            verbose_logger.exception(
                f"litellm.litellm_core_utils.llm_cost_calc.utils.py::calculate_cost_per_component(): Exception occured - {cost_per_unit}\nDefaulting to 0.0"
            )

    # If the service tier key doesn't exist or is None, try to fall back to the standard key
    if cost_per_unit is None:
        # Check if any service tier suffix exists in the cost key using ServiceTier enum
        for service_tier in ServiceTier:
            suffix = f"_{service_tier.value}"
            if suffix in cost_key:
                # Extract the base key by removing the matched suffix
                base_key = cost_key.replace(suffix, "")
                fallback_cost = model_info.get(base_key)
                if isinstance(fallback_cost, float):
                    return fallback_cost
                if isinstance(fallback_cost, int):
                    return float(fallback_cost)
                if isinstance(fallback_cost, str):
                    try:
                        return float(fallback_cost)
                    except ValueError:
                        verbose_logger.exception(
                            f"litellm.litellm_core_utils.llm_cost_calc.utils.py::_get_cost_per_unit(): Exception occured - {fallback_cost}\nDefaulting to 0.0"
                        )
                break  # Only try the first matching suffix

    return default_value

