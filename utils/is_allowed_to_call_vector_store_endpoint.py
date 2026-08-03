from typing import Optional

def is_allowed_to_call_vector_store_endpoint(
    provider: LlmProviders,
    index_name: str,
    request: Request,
    user_api_key_dict: UserAPIKeyAuth,
) -> Optional[Literal[True]]:
    """
    Check if the user is allowed to call the vector store endpoint.

    Cover:
    1. Creating a vector store index
    2. Reading a vector store index (Search / List / Get)
    """
    if (
        user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN
        or user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    ):
        return True
    # check what allowed permissions are for the key
    key_metadata = user_api_key_dict.metadata
    team_metadata = user_api_key_dict.team_metadata

    provider_config = ProviderConfigManager.get_provider_vector_stores_config(
        provider=provider
    )
    if provider_config is None:
        return None

    provider_vector_store_endpoints = (
        provider_config.get_vector_store_endpoints_by_type()
    )

    # Inline import — auth_utils participates in a proxy import cycle.
    from litellm.proxy.auth.auth_utils import get_request_route  # noqa: PLC0415

    request_route = get_request_route(request)

    if _is_vector_store_index_lifecycle_request(
        request_method=request.method,
        request_path=request_route,
        index_name=index_name,
    ):
        operation_label: Literal["create", "delete", "update"] = "create"
        if request.method == "DELETE":
            operation_label = "delete"
        elif request.method in ("PUT", "PATCH"):
            operation_label = "update"
        assert_proxy_admin_for_vector_store_index_management(
            user_api_key_dict,
            operation=operation_label,
        )
        return True

    # Determine the permission type based on the request
    permission_type = None
    for endpoint in provider_vector_store_endpoints["read"]:
        if request.method == endpoint[0] and _does_endpoint_match(
            endpoint[1], request_route
        ):
            permission_type = "read"
            break

    if permission_type is None:
        for endpoint in provider_vector_store_endpoints["write"]:
            if request.method == endpoint[0] and _does_endpoint_match(
                endpoint[1], request_route
            ):
                permission_type = "write"
                break

    if permission_type is None:
        raise HTTPException(
            status_code=403,
            detail=(
                f"User does not have permission to call vector store endpoint "
                f"{index_name}. Ask your administrator to add the necessary "
                "permissions to your API key/Team."
            ),
        )

    # Check if key has specific permission for allowed_vector_store_indexes
    has_permission = check_vector_store_permission(
        index_name=index_name,
        permission=permission_type,
        key_metadata=key_metadata,
        team_metadata=team_metadata,
    )

    if not has_permission:
        raise HTTPException(
            status_code=403,
            detail=f"User does not have permission to call vector store endpoint {index_name}. Ask your administrator to add the necessary permissions to your API key/Team.",
        )

    return has_permission

