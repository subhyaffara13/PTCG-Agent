
def _get_onboarding_claims_from_request(request: Request) -> dict:
    global master_key, general_settings

    if master_key is None:
        raise ProxyException(
            message="Master Key not set for Proxy. Please set Master Key to use Admin UI. Set `LITELLM_MASTER_KEY` in .env or set general_settings:master_key in config.yaml.  https://docs.litellm.ai/docs/proxy/virtual_keys. If set, use `--detailed_debug` to debug issue.",
            type=ProxyErrorTypes.auth_error,
            param="master_key",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    auth_header_name = general_settings.get("litellm_key_header_name", "Authorization")
    onboarding_auth_header = request.headers.get(auth_header_name)
    if onboarding_auth_header is None:
        raise HTTPException(
            status_code=401,
            detail={"error": "Missing onboarding session for invitation link."},
        )
    onboarding_token = onboarding_auth_header
    if onboarding_token.lower().startswith("bearer "):
        onboarding_token = onboarding_token.split(" ", 1)[1]

    import jwt

    try:
        return jwt.decode(
            onboarding_token,
            master_key,
            algorithms=["HS256"],
        )
    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid onboarding session for invitation link."},
        )

