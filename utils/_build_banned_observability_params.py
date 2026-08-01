
def _build_banned_observability_params() -> FrozenSet[str]:
    """Derive the observability ban list from the canonical allowlist.

    ``_supported_callback_params`` and ``_request_blocked_callback_params`` in
    ``litellm/litellm_core_utils/initialize_dynamic_callback_params.py`` is
    the single place that enumerates every observability field integrations
    resolve from kwargs/metadata, plus fields that integration code explicitly
    blocks from request-supplied callback params. Subtract the small set of
    informational fields (``_SAFE_CLIENT_CALLBACK_PARAMS``) and union with the
    extras the canonical allowlist hasn't caught up to yet. New integrations
    added to the canonical allowlist are banned by default, which is the safe
    failure mode.
    """
    from litellm.litellm_core_utils.initialize_dynamic_callback_params import (
        _request_blocked_callback_params,
        _supported_callback_params,
    )

    return (
        (frozenset(_supported_callback_params) - _SAFE_CLIENT_CALLBACK_PARAMS)
        | frozenset(_request_blocked_callback_params)
        | _EXTRA_BANNED_OBSERVABILITY_PARAMS
    )

