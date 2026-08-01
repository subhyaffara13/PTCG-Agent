
def _get_combined_custom_metadata_from_standard_logging_payload(
    standard_logging_payload: Optional[dict],
) -> Dict[str, Any]:
    """
    Combine the metadata sources that can supply custom Prometheus labels.
    """
    if not isinstance(standard_logging_payload, dict):
        return {}

    standard_logging_metadata = standard_logging_payload.get("metadata") or {}
    if not isinstance(standard_logging_metadata, dict):
        return {}

    requester_metadata = standard_logging_metadata.get("requester_metadata")
    user_api_key_auth_metadata = standard_logging_metadata.get(
        "user_api_key_auth_metadata"
    )
    spend_logs_metadata = standard_logging_metadata.get("spend_logs_metadata")

    return {
        **(requester_metadata if isinstance(requester_metadata, dict) else {}),
        **(
            user_api_key_auth_metadata
            if isinstance(user_api_key_auth_metadata, dict)
            else {}
        ),
        **(spend_logs_metadata if isinstance(spend_logs_metadata, dict) else {}),
    }

