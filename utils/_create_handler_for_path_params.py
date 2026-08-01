
def _create_handler_for_path_params(
    path_params: List[str],
    route_type: str,
    returns_binary: bool = False,
    is_multipart: bool = False,
):
    """
    Dynamically create a handler with the correct path parameter signature.
    """
    # For binary content endpoints, use a different handler
    if returns_binary and path_params == ["container_id", "file_id"]:

        async def handler_binary_content(
            request: Request,
            container_id: str,
            file_id: str,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
        ):
            return await _process_binary_request(
                request=request,
                fastapi_response=fastapi_response,
                container_id=container_id,
                file_id=file_id,
                user_api_key_dict=user_api_key_dict,
            )

        return handler_binary_content

    # For multipart file upload endpoints
    if is_multipart:

        async def handler_multipart_upload(
            request: Request,
            container_id: str,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
        ):
            return await _process_multipart_upload_request(
                request=request,
                fastapi_response=fastapi_response,
                user_api_key_dict=user_api_key_dict,
                route_type=route_type,
                container_id=container_id,
            )

        return handler_multipart_upload

    # Create handlers for different path parameter combinations
    if path_params == ["container_id"]:

        async def handler_container_id(
            request: Request,
            container_id: str,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
        ):
            return await _process_request(
                request=request,
                fastapi_response=fastapi_response,
                user_api_key_dict=user_api_key_dict,
                route_type=route_type,
                path_params={"container_id": container_id},
            )

        return handler_container_id

    elif path_params == ["container_id", "file_id"]:

        async def handler_container_file(
            request: Request,
            container_id: str,
            file_id: str,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
        ):
            return await _process_request(
                request=request,
                fastapi_response=fastapi_response,
                user_api_key_dict=user_api_key_dict,
                route_type=route_type,
                path_params={"container_id": container_id, "file_id": file_id},
            )

        return handler_container_file

    else:
        # Fallback for no path params
        async def handler_no_params(
            request: Request,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
        ):
            return await _process_request(
                request=request,
                fastapi_response=fastapi_response,
                user_api_key_dict=user_api_key_dict,
                route_type=route_type,
                path_params={},
            )

        return handler_no_params

