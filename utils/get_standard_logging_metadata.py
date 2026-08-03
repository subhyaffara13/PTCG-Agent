from typing import Any, Dict, Optional

def get_standard_logging_metadata(
    metadata: Optional[Dict[str, Any]],
) -> StandardLoggingMetadata:
    """
    Clean and filter the metadata dictionary to include only the specified keys in StandardLoggingMetadata.

    Args:
        metadata (Optional[Dict[str, Any]]): The original metadata dictionary.

    Returns:
        StandardLoggingMetadata: A StandardLoggingMetadata object containing the cleaned metadata.

    Note:
        - If the input metadata is None or not a dictionary, an empty StandardLoggingMetadata object is returned.
        - If 'user_api_key' is present in metadata and is a valid SHA256 hash, it's stored as 'user_api_key_hash'.
    """
    # Initialize with default values
    clean_metadata = StandardLoggingMetadata(
        user_api_key_hash=None,
        user_api_key_alias=None,
        user_api_key_spend=None,
        user_api_key_max_budget=None,
        user_api_key_budget_reset_at=None,
        user_api_key_team_id=None,
        user_api_key_org_id=None,
        user_api_key_org_alias=None,
        user_api_key_project_id=None,
        user_api_key_project_alias=None,
        user_api_key_user_id=None,
        user_api_key_user_email=None,
        user_api_key_team_alias=None,
        spend_logs_metadata=None,
        requester_ip_address=None,
        user_agent=None,
        requester_metadata=None,
        user_api_key_end_user_id=None,
        prompt_management_metadata=None,
        applied_guardrails=None,
        mcp_tool_call_metadata=None,
        vector_store_request_metadata=None,
        usage_object=None,
        requester_custom_headers=None,
        user_api_key_request_route=None,
        cold_storage_object_key=None,
        user_api_key_auth_metadata=None,
        team_alias=None,
        team_id=None,
    )
    if isinstance(metadata, dict):
        # Update the clean_metadata with values from input metadata that match StandardLoggingMetadata fields
        for key in StandardLoggingMetadata.__annotations__.keys():
            if key in metadata:
                clean_metadata[key] = metadata[key]  # type: ignore

        if metadata.get("user_api_key") is not None:
            if is_valid_sha256_hash(str(metadata.get("user_api_key"))):
                clean_metadata["user_api_key_hash"] = metadata.get(
                    "user_api_key"
                )  # this is the hash
    return clean_metadata

