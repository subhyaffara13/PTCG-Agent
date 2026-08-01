
def assert_proxy_admin_for_vector_store_index_management(
    user_api_key_dict: UserAPIKeyAuth,
    *,
    operation: Literal["create", "delete", "update"] = "create",
) -> None:
    """Raise 403 unless the caller is a proxy admin."""
    if _is_proxy_admin(user_api_key_dict):
        return
    raise HTTPException(
        status_code=403,
        detail=(
            f"Only proxy admins can {operation} vector store indexes. "
            "Contact your LiteLLM administrator."
        ),
    )

