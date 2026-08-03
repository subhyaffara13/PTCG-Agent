from typing import Optional

def prepare_data_with_credentials(
    data: dict,
    credentials: dict,
    file_id: Optional[str] = None,
    include_internal_credentials: bool = False,
) -> None:
    """
    Update data dictionary with model credentials (in-place).

    Args:
        data: Data dictionary to update
        credentials: Credentials from router
        file_id: Optional original file_id to set (for decoded file IDs)
        include_internal_credentials: Preserve an immutable server-side snapshot
            for code paths that must distinguish proxy config from request params.
    """
    data.update(credentials)
    if include_internal_credentials:
        data["_litellm_internal_model_credentials"] = MappingProxyType(
            dict(credentials)
        )
    data.pop("custom_llm_provider", None)

    if file_id is not None:
        data["file_id"] = file_id

