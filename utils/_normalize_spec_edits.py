
def _normalize_spec_edits(
    *,
    context_management_spec: Any,
    drop_params: Optional[bool],
) -> Optional[List[Dict[str, Any]]]:
    """Return the normalized ``edits`` list, or ``None`` if the polyfill won't run.

    Delegates spec-shape normalization to the dispatcher's ``_normalize_spec``
    so the prediction here can't drift from what the dispatcher actually does.
    """
    if not context_management_spec:
        return None

    effective_drop_params = (
        drop_params if drop_params is not None else litellm.drop_params
    )
    if effective_drop_params:
        return None

    from litellm.llms.anthropic.experimental_pass_through.context_management.dispatcher import (
        _normalize_spec,
    )

    try:
        return _normalize_spec(context_management_spec)
    except Exception:
        return None

