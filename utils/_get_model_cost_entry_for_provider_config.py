from typing import Any, Dict

def _get_model_cost_entry_for_provider_config(
    model: str,
    provider: LlmProviders,
) -> Dict[str, Any]:
    candidate_keys = (model, f"{provider.value}/{model}")
    for model_key in candidate_keys:
        model_info = litellm.model_cost.get(model_key)
        if model_info is not None:
            return model_info

    bundled_model_cost = _get_bundled_model_cost_map()
    for model_key in candidate_keys:
        model_info = bundled_model_cost.get(model_key)
        if model_info is not None:
            return model_info
    return {}

