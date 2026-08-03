from typing import Any, Dict, Optional

def _estimate_image_generation_cost(
    request_body: dict,
    model_info: Dict[str, Any],
) -> Optional[float]:
    """
    Reserve `n × per-image cost` for image-generation requests so concurrent
    requests against a depleted budget cannot all slip past the admission gate
    onto the provider. Token-based pricing (e.g. gpt-image-1) is handled by
    the chat-route token path; per-pixel and size/quality-tiered pricing
    (DALL-E 2 size variants, premium tiers) are not handled here and fall
    through to read-time enforcement.

    The "output" vs "input" cost-per-image naming is inconsistent across
    providers — OpenAI's dall-e-3 entry uses ``input_cost_per_image`` while
    aiml/dall-e-3 uses ``output_cost_per_image`` — so both are summed.
    """
    # Gate strictly on `mode`. Several chat and embedding models carry
    # ``input_cost_per_image`` / ``output_cost_per_image`` to price multimodal
    # *vision input* (e.g. ``gemini-3.1-pro-preview``, ``azure/gpt-realtime-*``,
    # ``amazon.titan-embed-image-v1``). Falling back to "treat as image-gen if
    # an image cost field is present" would short-circuit the token-priced
    # path for those models and reserve a fraction of a cent instead of the
    # true per-token cost. All real image-generation entries in
    # ``model_prices_and_context_window.json`` carry ``mode: image_generation``
    # or ``mode: image_edit``, so the field-presence fallback is unnecessary.
    if model_info.get("mode") not in ("image_generation", "image_edit"):
        return None

    output_cost_per_image = _to_float(model_info.get("output_cost_per_image"))
    input_cost_per_image = _to_float(model_info.get("input_cost_per_image"))
    cost_per_image = (output_cost_per_image or 0.0) + (input_cost_per_image or 0.0)
    if cost_per_image <= 0:
        return None

    n = _to_int(request_body.get("n")) or 1
    return cost_per_image * max(n, 1)

