from typing import Optional

def _is_explicitly_disabled_factory(
    model: str, custom_llm_provider: Optional[str], key: str
) -> bool:
    """Return True only when the model map explicitly sets *key* to ``False``.

    This is the opt-out mirror of :func:`_supports_factory`.  Where
    ``_supports_factory`` requires an explicit ``True`` to return ``True``,
    this function requires an explicit ``False``.  A missing key (``None``)
    is treated as *not* disabled so that unknown or newly-added models are
    allowed through without any model-map entry.

    Uses the same ``get_llm_provider`` → ``_get_model_info_helper`` chain as
    ``_supports_factory`` so caching, fallback, and normalisation improvements
    apply here automatically.
    """
    try:
        model, custom_llm_provider, _, _ = litellm.get_llm_provider(
            model=model, custom_llm_provider=custom_llm_provider
        )
        model_info = _get_model_info_helper(
            model=model, custom_llm_provider=custom_llm_provider
        )
        val = model_info.get(key)
        if val is False:
            return True
        if val is None:
            bare_model_key = _get_model_cost_key(model)
            if bare_model_key is not None:
                bare_entry = litellm.model_cost.get(bare_model_key) or {}
                if bare_entry.get(key) is False:
                    return True
        return False
    except Exception as e:
        verbose_logger.debug(
            f"Model not found or error in checking {key} disabled state. "
            f"You passed model={model}, custom_llm_provider={custom_llm_provider}. "
            f"Error: {str(e)}"
        )
        return False

