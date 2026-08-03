from typing import Optional

def check_complete_credentials(request_body: dict) -> bool:
    """
    if 'api_base' in request body. Check if complete credentials given. Prevent malicious attacks.

    Supplying an ``api_key`` is necessary but not sufficient: even with
    credentials supplied, an ``api_base`` / ``base_url`` that resolves to a
    private/internal/cloud-metadata address would still allow the proxy to
    be used as an SSRF pivot. Validate any URL fields here so the gate
    can't be bypassed with ``api_key=anything`` plus a malicious target.
    """
    given_model: Optional[str] = None

    given_model = request_body.get("model")
    if given_model is None:
        return False

    if (
        "sagemaker" in given_model
        or "bedrock" in given_model
        or "vertex_ai" in given_model
        or "vertex_ai_beta" in given_model
    ):
        # complex credentials - easier to make a malicious request
        return False

    api_key_value = request_body.get("api_key")
    if not (api_key_value and isinstance(api_key_value, str) and api_key_value.strip()):
        return False

    # ``validate_url`` itself doesn't consult the toggle; ``safe_get`` /
    # ``async_safe_get`` do. Mirror that here so admins who explicitly
    # disabled URL validation (e.g. for an internal Ollama endpoint they
    # accept the SSRF risk for) aren't blocked at the proxy boundary.
    if getattr(litellm, "user_url_validation", False):
        for url_field in ("api_base", "base_url"):
            url_value = request_body.get(url_field)
            if not url_value or not isinstance(url_value, str):
                continue
            try:
                validate_url(url_value)
            except SSRFError as e:
                raise ValueError(
                    f"Rejected request: client-side {url_field}={url_value!r} "
                    f"is rejected by the SSRF guard ({e})."
                )

    return True

