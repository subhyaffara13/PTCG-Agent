
def extract_model_id_from_unified_id(
    unified_id: str,
) -> Optional[str]:
    """
    Extract model ID from a unified resource ID.

    Args:
        unified_id: The unified resource ID (decoded or encoded)

    Returns:
        Model ID string or None

    Example:
        unified_id = "litellm_proxy:vector_store;...;model_id,gpt-4-model-id;..."
        returns: "gpt-4-model-id"
    """
    try:
        # Ensure unified_id is a string
        if not isinstance(unified_id, str):
            return None

        # Decode if it's base64 encoded
        decoded_id = is_base64_encoded_unified_id(unified_id)
        if decoded_id:
            unified_id = decoded_id

        # Extract model ID. Anchor to a field boundary (start of string or
        # after `;`) so this regex doesn't substring-match the `model_id,`
        # inside file_id encodings' `llm_output_file_model_id,<deployment_uuid>`
        # field — that would feed the deployment UUID as a model candidate
        # into the team-access check and 403 every team-BYOK file attach
        # with `Tried to access <uuid>` (LIT-3244 patch/1.86.0 second-order
        # finding).
        match = re.search(r"(?:^|;)model_id,([^;]+)", unified_id)
        if match:
            return match.group(1).strip()

        return None
    except Exception:
        return None

