
def is_allowed_to_call_vector_store_files_endpoint(
    provider: LlmProviders,
    vector_store_id: str,
    request: Request,
    user_api_key_dict: UserAPIKeyAuth,
) -> Optional[Literal[True]]:
    if (
        user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN
        or user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    ):
        return True

    key_metadata = user_api_key_dict.metadata
    team_metadata = user_api_key_dict.team_metadata

    provider_config = ProviderConfigManager.get_provider_vector_store_files_config(
        provider=provider
    )
    if provider_config is None:
        return None

    provider_vector_store_endpoints = (
        provider_config.get_vector_store_file_endpoints_by_type()
    )

    # Inline import — auth_utils participates in a proxy import cycle.
    from litellm.proxy.auth.auth_utils import get_request_route  # noqa: PLC0415

    request_route = get_request_route(request)

    permission_type: Optional[str] = None
    for endpoint in provider_vector_store_endpoints.get("read", ()):
        if request.method == endpoint[0] and _does_endpoint_match(
            endpoint[1], request_route
        ):
            permission_type = "read"
            break

    if permission_type is None:
        for endpoint in provider_vector_store_endpoints.get("write", ()):
            if request.method == endpoint[0] and _does_endpoint_match(
                endpoint[1], request_route
            ):
                permission_type = "write"
                break

    if permission_type is None:
        return None

    has_permission = check_vector_store_permission(
        index_name=vector_store_id,
        permission=permission_type,
        key_metadata=key_metadata,
        team_metadata=team_metadata,
    )

    if not has_permission:
        raise HTTPException(
            status_code=403,
            detail=f"User does not have permission to call vector store file endpoint {vector_store_id}. Ask your administrator to add the necessary permissions to your API key/Team.",
        )

    return has_permission

