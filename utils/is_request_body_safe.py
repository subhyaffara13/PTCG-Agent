
def is_request_body_safe(
    request_body: dict, general_settings: dict, llm_router: Optional[Router], model: str
) -> bool:
    """
    Check if the request body is safe.

    A malicious user can set the ﻿api_base to their own domain and invoke POST /chat/completions to intercept and steal the OpenAI API key.
    Relevant issue: https://huntr.com/bounties/4001e1a2-7b7a-4776-a3ae-e6692ec3d997

    The blocklist is enforced unconditionally. Legitimate clientside
    credential / endpoint passthrough goes through one of the two
    explicit admin opt-ins (``general_settings.allow_client_side_credentials``
    proxy-wide or ``configurable_clientside_auth_params`` per deployment).
    Historically there was a third, *implicit*, *caller-controlled* path:
    ``check_complete_credentials`` returned True when the caller supplied
    any non-empty ``api_key``, which made the entire blocklist a no-op.
    That bypass turned every missing entry on the blocklist into an
    exploitable SSRF / credential-exfil hole — see GHSA-jh89-88fc-qrfp,
    GHSA-3frq-6r6h-7j64, and the chain of veria-admin findings (Dv_m860l,
    b_yRJeQ5, stN90yjP, LBlyOAc8, U2TD78kg). Removed: the blocklist now
    has a single, predictable failure mode for missing entries (a 400),
    not a credential leak.

    Iterative single-level descent into ``_NESTED_CONFIG_KEYS`` (rather
    than recursion) covers nested-config attacks like Milvus's
    ``litellm_embedding_config.api_base`` (VERIA-6) without exposing a
    recursion-depth DoS surface.
    """
    _check_banned_params(request_body, general_settings, llm_router, model)
    for nested_key in _NESTED_CONFIG_KEYS:
        nested = _coerce_metadata_to_dict(request_body.get(nested_key))
        if nested is not None:
            _check_banned_params(nested, general_settings, llm_router, model)
    for metadata_key in _NESTED_METADATA_KEYS:
        metadata = _coerce_metadata_to_dict(request_body.get(metadata_key))
        if metadata is not None:
            _check_banned_params(metadata, general_settings, llm_router, model)
    return True

