
def _sanitize_request_body_for_spend_logs_payload(
    request_body: dict,
    visited: Optional[set] = None,
    max_string_length_prompt_in_db: Optional[int] = None,
) -> dict:
    """
    Recursively sanitize request body to prevent logging large base64 strings or other large values.
    Truncates strings longer than MAX_STRING_LENGTH_PROMPT_IN_DB characters and handles nested dictionaries.

    Also strips keys listed in _SENSITIVE_REQUEST_BODY_KEYS (e.g. secret_fields
    which contains raw HTTP headers including Authorization tokens).
    """
    from litellm.constants import (
        LITELLM_TRUNCATED_PAYLOAD_FIELD,
        LITELLM_TRUNCATION_DB_SAFEGUARD_NOTE,
    )

    if visited is None:
        visited = set()
    if max_string_length_prompt_in_db is None:
        max_string_length_prompt_in_db = _get_max_string_length_prompt_in_db()

    # Get the object's memory address to track visited objects
    obj_id = id(request_body)
    if obj_id in visited:
        return {}
    visited.add(obj_id)

    def _sanitize_value(value: Any) -> Any:
        if isinstance(value, dict):
            return _sanitize_request_body_for_spend_logs_payload(
                value, visited, max_string_length_prompt_in_db
            )
        elif isinstance(value, list):
            return [_sanitize_value(item) for item in value]
        elif isinstance(value, str):
            if len(value) > max_string_length_prompt_in_db:
                # Keep 35% from beginning and 65% from end (end is usually more important)
                # This split ensures we keep more context from the end of conversations
                start_ratio = 0.35
                end_ratio = 0.65

                # Calculate character distribution
                start_chars = int(max_string_length_prompt_in_db * start_ratio)
                end_chars = int(max_string_length_prompt_in_db * end_ratio)

                # Ensure we don't exceed the total limit
                total_keep = start_chars + end_chars
                if total_keep > max_string_length_prompt_in_db:
                    end_chars = max_string_length_prompt_in_db - start_chars

                # If the string length is less than what we want to keep, just truncate normally
                if len(value) <= max_string_length_prompt_in_db:
                    return value

                # Calculate how many characters are being skipped
                skipped_chars = len(value) - total_keep

                # Build the truncated string: beginning + truncation marker + end
                truncated_value = (
                    f"{value[:start_chars]}"
                    f"... ({LITELLM_TRUNCATED_PAYLOAD_FIELD} skipped {skipped_chars} chars. "
                    f"{LITELLM_TRUNCATION_DB_SAFEGUARD_NOTE}) ..."
                    f"{value[-end_chars:]}"
                )
                return truncated_value
            return value
        return value

    return {
        k: _sanitize_value(v)
        for k, v in request_body.items()
        if k not in _SENSITIVE_REQUEST_BODY_KEYS
    }

