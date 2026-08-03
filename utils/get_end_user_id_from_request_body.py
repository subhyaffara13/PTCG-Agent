from typing import Any, Optional, Union

def get_end_user_id_from_request_body(
    request_body: dict, request_headers: Optional[dict] = None
) -> Optional[str]:
    # Import general_settings here to avoid potential circular import issues at module level
    # and to ensure it's fetched at runtime.
    from litellm.proxy.proxy_server import general_settings

    # Check 1: Standard customer ID headers (always checked, no configuration required)
    customer_id = _get_customer_id_from_standard_headers(
        request_headers=request_headers
    )
    if customer_id is not None:
        return customer_id

    # Check 2: Follow the user header mappings feature, if not found, then check for deprecated user_header_name (only if request_headers is provided)
    # User query: "system not respecting user_header_name property"
    # This implies the key in general_settings is 'user_header_name'.
    if request_headers is not None:
        custom_header_name_to_check: Optional[Union[list, str]] = None

        # Prefer user mappings (new behavior)
        user_id_mapping = general_settings.get("user_header_mappings", None)
        if user_id_mapping:
            custom_header_name_to_check = get_customer_user_header_from_mapping(
                user_id_mapping
            )

        # Fallback to deprecated user_header_name if mapping did not specify
        if not custom_header_name_to_check:
            user_id_header_config_key = "user_header_name"
            value = general_settings.get(user_id_header_config_key)
            if isinstance(value, str) and value.strip() != "":
                custom_header_name_to_check = value

        # If we have a header name to check, try to read it from request headers
        if isinstance(custom_header_name_to_check, list):
            headers_lower = {k.lower(): v for k, v in request_headers.items()}
            for expected_header in custom_header_name_to_check:
                user_id_str = _coerce_user_id_to_str(headers_lower.get(expected_header))
                if user_id_str:
                    return user_id_str

        elif isinstance(custom_header_name_to_check, str):
            for header_name, header_value in request_headers.items():
                if header_name.lower() == custom_header_name_to_check.lower():
                    user_id_str = _coerce_user_id_to_str(header_value)
                    if user_id_str:
                        return user_id_str

    # Check 3: 'user' field in request_body (commonly OpenAI)
    if "user" in request_body:
        user_id_str = _coerce_user_id_to_str(request_body["user"])
        if user_id_str:
            return user_id_str

    def _as_dict(value: Any) -> dict:
        # metadata / litellm_metadata can arrive as JSON strings from
        # multipart/form-data or extra_body; coerce so string-encoded
        # payloads can't evade end-user attribution.
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            parsed = safe_json_loads(value)
            return parsed if isinstance(parsed, dict) else {}
        return {}

    # Check 4: 'litellm_metadata.user' in request_body (commonly Anthropic)
    litellm_metadata = _as_dict(request_body.get("litellm_metadata"))
    user_id_str = _coerce_user_id_to_str(litellm_metadata.get("user"))
    if user_id_str:
        return user_id_str

    # Check 5: 'metadata.user_id' in request_body (another common pattern)
    metadata_dict = _as_dict(request_body.get("metadata"))
    user_id_str = _coerce_user_id_to_str(metadata_dict.get("user_id"))
    if user_id_str:
        return user_id_str

    # Check 6: 'safety_identifier' in request body (OpenAI Responses API parameter)
    # SECURITY NOTE: safety_identifier can be set by any caller in the request body.
    # Only use this for end-user identification in trusted environments where you control
    # the calling application. For untrusted callers, prefer using headers or server-side
    # middleware to set the end_user_id to prevent impersonation.
    user_id_str = _coerce_user_id_to_str(request_body.get("safety_identifier"))
    if user_id_str:
        return user_id_str

    return None

