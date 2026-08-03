from typing import List, Optional

def _supports_nova_canvas_image_edit_from_model_cost(model: str) -> bool:
    """
    True when model_cost has supports_nova_canvas_image_edit for a resolved catalog key.

    get_model_info / ModelInfoBase omit arbitrary JSON keys, so we read model_cost
    directly (same idea as supports_* bare_entry fallback).
    """
    import litellm as _litellm

    if not model:
        return False

    seen: set[str] = set()
    candidates: List[str] = []

    def _add(name: Optional[str]) -> None:
        if name and name not in seen:
            seen.add(name)
            candidates.append(name)

    _add(model)
    if "/" in model:
        suffix = model.split("/")[-1]
        _add(suffix)
        _add(f"bedrock/{suffix}")

    # Cross-region inference ids (e.g. us.amazon.nova-canvas-v1:0) share pricing with
    # the base model id (amazon.nova-canvas-v1:0) in model_cost.
    try:
        from litellm.llms.bedrock.common_utils import BedrockModelInfo

        base_model = BedrockModelInfo.get_base_model(model)
        if base_model and base_model != model:
            _add(base_model)
            _add(f"bedrock/{base_model}")
    except Exception:
        pass

    try:
        potential = _get_potential_model_names(model=model, custom_llm_provider=None)
        for field in (
            "combined_model_name",
            "combined_stripped_model_name",
            "stripped_model_name",
            "split_model",
        ):
            raw = potential.get(field)
            if isinstance(raw, str):
                _add(raw)
    except Exception:
        pass

    for name in candidates:
        key = _get_model_cost_key(name)
        if key is None:
            continue
        entry = _litellm.model_cost.get(key) or {}
        if entry.get("supports_nova_canvas_image_edit") is True:
            return True
    return False

