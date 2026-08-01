
def extract_opik_metadata(
    litellm_metadata: Dict[str, Any],
    standard_logging_metadata: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Merge Opik metadata from three sources in increasing priority order:

      1. user_api_key_auth_metadata– lowest priority (operator-level defaults)
      2. litellm_metadata (request)– overrides auth-key defaults
      3. requester_metadata – highest priority (e.g. proxy header overrides)

    Args:
        litellm_metadata: Metadata from litellm_params.mak
        standard_logging_metadata: Metadata from standard_logging_object.

    Returns:
        Merged Opik metadata dictionary.
    """
    # Start with auth-key defaults (lowest priority).
    auth_meta = standard_logging_metadata.get("user_api_key_auth_metadata") or {}
    opik_meta = (auth_meta.get("opik") or {}).copy()

    # Request-level values override auth-key defaults.
    request_opik = litellm_metadata.get("opik") or {}
    opik_meta.update(request_opik)

    # Requester-level values win over everything else.
    requester_metadata = standard_logging_metadata.get("requester_metadata", {}) or {}
    requester_opik = requester_metadata.get("opik", {}) or {}
    if requester_opik:
        opik_meta.update(requester_opik)

    _logging.verbose_logger.debug(
        f"litellm_opik_metadata - {json.dumps(opik_meta, default=str)}"
    )

    return opik_meta

