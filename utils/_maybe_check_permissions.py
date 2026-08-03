from typing import Optional

def _maybe_check_permissions(
    *,
    provider: Optional[LlmProviders],
    vector_store_id: str,
    request: Request,
    user_api_key_dict: UserAPIKeyAuth,
) -> None:
    if provider is None:
        return
    metadata = user_api_key_dict.metadata or {}
    team_metadata = user_api_key_dict.team_metadata or {}
    if not metadata.get("allowed_vector_store_indexes") and not team_metadata.get(
        "allowed_vector_store_indexes"
    ):
        return
    is_allowed_to_call_vector_store_files_endpoint(
        provider=provider,
        vector_store_id=vector_store_id,
        request=request,
        user_api_key_dict=user_api_key_dict,
    )

