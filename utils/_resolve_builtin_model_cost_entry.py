from typing import Any, Dict, List, Optional

def _resolve_builtin_model_cost_entry(
    key: str, provider: str
) -> Optional[Dict[str, Any]]:
    """Best-effort lookup of a built-in ``model_cost`` entry for a custom key
    whose shape ``get_model_info`` cannot resolve (double provider prefixes
    like ``bedrock/bedrock/us.anthropic.claude-sonnet-4-6`` or region aliases).

    Returns a copy of the matching entry so the caller can inherit its defaults
    (most importantly cache pricing) without mutating the shared built-in.
    Returns ``None`` when no safe match exists.
    """
    candidates: List[str] = []
    segments = key.split("/")
    idx = 0
    while idx < len(segments) - 1 and segments[idx] in LlmProvidersSet:
        idx += 1
        candidates.append("/".join(segments[idx:]))

    base = candidates[-1] if candidates else key
    for region_prefix in _BEDROCK_REGION_PREFIXES:
        if base.startswith(region_prefix):
            candidates.append(base[len(region_prefix) :])

    if provider:
        stripped = _strip_model_name(model=base, custom_llm_provider=provider)
        if stripped != base:
            candidates.append(stripped)

    for candidate in candidates:
        entry = litellm.model_cost.get(candidate)
        if entry is not None and entry.get("litellm_provider") is not None:
            return dict(entry)
    return None

