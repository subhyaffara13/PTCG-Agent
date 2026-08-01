
def validate_oci_environment(
    headers: dict,
    optional_params: dict,
    api_key: Optional[str] = None,
) -> dict:
    """
    Populate common OCI request headers (content-type, user-agent).

    Full credential validation is deferred to signing time so that credentials
    supplied via environment variables are resolved at call time rather than
    at construction time.
    """
    headers.setdefault("content-type", "application/json")
    headers.setdefault("user-agent", f"litellm/{_litellm_version}")
    return headers

