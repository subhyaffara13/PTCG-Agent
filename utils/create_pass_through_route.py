
def create_pass_through_route(
    endpoint,
    target: str,
    custom_headers: Optional[Mapping[str, Any]] = None,
    _forward_headers: Optional[bool] = False,
    _merge_query_params: Optional[bool] = False,
    dependencies: Optional[List] = None,
    include_subpath: Optional[bool] = False,
    cost_per_request: Optional[float] = None,
    custom_llm_provider: Optional[str] = None,
    is_streaming_request: Optional[bool] = False,
    query_params: Optional[dict] = None,
    default_query_params: Optional[dict] = None,
    guardrails: Optional[Dict[str, Any]] = None,
    config_file_path: Optional[str] = None,
    timeout: Optional[float] = None,
):
    # check if target is an adapter.py or a url
    from litellm._uuid import uuid
    from litellm.proxy.types_utils.utils import get_instance_fn

    try:
        if isinstance(target, CustomLogger):
            adapter = target
        else:
            adapter = get_instance_fn(value=target, config_file_path=config_file_path)
        adapter_id = str(uuid.uuid4())
        litellm.adapters = [{"id": adapter_id, "adapter": adapter}]

        async def endpoint_func(  # type: ignore
            request: Request,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
            subpath: str = "",  # captures sub-paths when include_subpath=True
        ):
            return await chat_completion_pass_through_endpoint(
                fastapi_response=fastapi_response,
                request=request,
                adapter_id=adapter_id,
                user_api_key_dict=user_api_key_dict,
            )

    except Exception:
        verbose_proxy_logger.debug("Defaulting to target being a url.")

        async def endpoint_func(  # type: ignore
            request: Request,
            fastapi_response: Response,
            user_api_key_dict: UserAPIKeyAuth = Depends(user_api_key_auth),
            subpath: str = "",  # captures sub-paths when include_subpath=True
        ):
            from litellm.proxy.auth.auth_utils import (  # noqa: PLC0415
                get_request_route,
            )
            from litellm.proxy.pass_through_endpoints.pass_through_endpoints import (
                InitPassThroughEndpointHelpers,
            )

            path = get_request_route(request)

            # Parse request data based on content type
            (
                query_params_data,
                custom_body_data,
                file_data,
                stream,
            ) = await _parse_request_data_by_content_type(request)

            if not InitPassThroughEndpointHelpers.is_registered_pass_through_route(
                route=path
            ):
                raise HTTPException(
                    status_code=404,
                    detail=f"Pass-through endpoint {endpoint} not found. This could have been deleted or not yet added to the proxy.",
                )

            passthrough_params = (
                InitPassThroughEndpointHelpers.get_registered_pass_through_route(
                    route=path, method=request.method
                )
            )
            if (
                passthrough_params is None
                and InitPassThroughEndpointHelpers.get_registered_pass_through_route(
                    route=path
                )
                is not None
            ):
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {request.method} is not allowed for pass-through endpoint {path}.",
                )
            target_params = {
                "target": target,
                "custom_headers": custom_headers,
                "forward_headers": _forward_headers,
                "merge_query_params": _merge_query_params,
                "cost_per_request": cost_per_request,
                "guardrails": None,
                "timeout": timeout,
            }

            if passthrough_params is not None:
                target_params.update(passthrough_params.get("passthrough_params", {}))

            # Extract and cast parameters with proper types
            param_target = target_params.get("target") or target
            param_custom_headers = target_params.get("custom_headers", custom_headers)
            param_forward_headers = target_params.get(
                "forward_headers", _forward_headers
            )
            param_merge_query_params = target_params.get(
                "merge_query_params", _merge_query_params
            )
            param_cost_per_request = target_params.get(
                "cost_per_request", cost_per_request
            )
            param_guardrails = target_params.get("guardrails", None)
            param_default_query_params = target_params.get("default_query_params", None)
            param_timeout = target_params.get("timeout", timeout)

            # Construct the full target URL with subpath if needed
            full_target = (
                HttpPassThroughEndpointHelpers.construct_target_url_with_subpath(
                    base_target=cast(str, param_target),
                    subpath=subpath,
                    include_subpath=include_subpath,
                )
            )

            # Ensure custom_headers is a dict. Botocore returns a HeadersDict
            # for SigV4-prepared requests, which is a Mapping but not a dict.
            headers_dict = (
                dict(param_custom_headers)
                if isinstance(param_custom_headers, Mapping)
                else {}
            )

            # Ensure query_params and custom_body are dicts or None
            final_query_params = (
                query_params_data if isinstance(query_params_data, dict) else {}
            )
            if query_params:
                final_query_params.update(query_params)
            # Programmatic callers set LITELLM_PASS_THROUGH_CUSTOM_BODY_STATE_KEY on
            # request.state (see Bedrock proxy). Parsed JSON envelope otherwise.
            state_custom_body: Optional[dict] = getattr(
                request.state,
                LITELLM_PASS_THROUGH_CUSTOM_BODY_STATE_KEY,
                None,
            )
            final_custom_body: Optional[dict] = None
            if isinstance(state_custom_body, dict):
                final_custom_body = state_custom_body
            elif isinstance(custom_body_data, dict):
                final_custom_body = custom_body_data

            try:
                return await pass_through_request(  # type: ignore
                    request=request,
                    target=full_target,
                    custom_headers=headers_dict,
                    user_api_key_dict=user_api_key_dict,
                    forward_headers=cast(Optional[bool], param_forward_headers),
                    merge_query_params=cast(Optional[bool], param_merge_query_params),
                    query_params=final_query_params,
                    default_query_params=cast(
                        Optional[dict], param_default_query_params
                    ),
                    stream=is_streaming_request or stream,
                    custom_body=final_custom_body,
                    cost_per_request=cast(Optional[float], param_cost_per_request),
                    custom_llm_provider=custom_llm_provider,
                    guardrails_config=cast(Optional[dict], param_guardrails),
                    timeout=cast(Optional[float], param_timeout),
                )
            finally:
                if hasattr(request.state, LITELLM_PASS_THROUGH_CUSTOM_BODY_STATE_KEY):
                    delattr(request.state, LITELLM_PASS_THROUGH_CUSTOM_BODY_STATE_KEY)
                if hasattr(request.state, LITELLM_PASS_THROUGH_RAW_BODY_STATE_KEY):
                    delattr(request.state, LITELLM_PASS_THROUGH_RAW_BODY_STATE_KEY)

    return endpoint_func

