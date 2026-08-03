import json
from typing import Any, Optional, Union

def llm_passthrough_route(
    *,
    method: str,
    endpoint: str,
    model: str,
    custom_llm_provider: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    request_query_params: Optional[dict] = None,
    request_headers: Optional[dict] = None,
    allm_passthrough_route: bool = False,
    content: Optional[Any] = None,
    data: Optional[dict] = None,
    files: Optional[RequestFiles] = None,
    json: Optional[Any] = None,
    params: Optional[QueryParamTypes] = None,
    cookies: Optional[CookieTypes] = None,
    client: Optional[Union[HTTPHandler, AsyncHTTPHandler]] = None,
    **kwargs,
) -> Union[
    httpx.Response,
    Coroutine[Any, Any, httpx.Response],
    Coroutine[Any, Any, Union[httpx.Response, AsyncGenerator[Any, Any]]],
    Generator[Any, Any, Any],
    AsyncGenerator[Any, Any],
]:
    """
    Pass through requests to the LLM APIs.

    Step 1. Build the request
    Step 2. Send the request
    Step 3. Return the response
    """
    from litellm.litellm_core_utils.get_litellm_params import get_litellm_params
    from litellm.types.utils import LlmProviders
    from litellm.utils import ProviderConfigManager

    _is_async = allm_passthrough_route

    litellm_logging_obj = cast("LiteLLMLoggingObj", kwargs.get("litellm_logging_obj"))

    model, custom_llm_provider, api_key, api_base = get_llm_provider(
        model=model,
        custom_llm_provider=custom_llm_provider,
        api_base=api_base,
        api_key=api_key,
    )

    litellm_params_dict = get_litellm_params(**kwargs)

    if client is None:
        from litellm.llms.custom_httpx.http_handler import (
            _get_httpx_client,
            get_async_httpx_client,
        )
        from litellm.passthrough.timeout_utils import resolve_llm_passthrough_timeout
        from litellm.types.llms.custom_http import httpxSpecialProvider

        resolved_timeout = resolve_llm_passthrough_timeout(
            kwargs=kwargs,
            litellm_params=litellm_params_dict,
        )
        if _is_async:
            client = get_async_httpx_client(
                llm_provider=httpxSpecialProvider.PassThroughEndpoint,
                params={"timeout": resolved_timeout},
            )
        else:
            client = _get_httpx_client(params={"timeout": resolved_timeout})

    # Add model_id to litellm_params if present in kwargs (for Bedrock Application Inference Profiles)
    if "model_id" in kwargs:
        litellm_params_dict["model_id"] = kwargs["model_id"]

    litellm_logging_obj.update_environment_variables(
        model=model,
        litellm_params=litellm_params_dict,
        optional_params={},
        endpoint=endpoint,
        custom_llm_provider=custom_llm_provider,
        request_data=data if data else json,
    )

    provider_config = cast(
        Optional["BasePassthroughConfig"], kwargs.get("provider_config")
    ) or ProviderConfigManager.get_provider_passthrough_config(
        provider=LlmProviders(custom_llm_provider),
        model=model,
    )
    if provider_config is None:
        raise Exception(f"Provider {custom_llm_provider} not found")

    updated_url, base_target_url = provider_config.get_complete_url(
        api_base=api_base,
        api_key=api_key,
        model=model,
        endpoint=endpoint,
        request_query_params=request_query_params,
        litellm_params=litellm_params_dict,
    )

    # [TODO: Refactor to bedrockpassthroughconfig] need to encode the id of application-inference-profile for bedrock
    if custom_llm_provider == "bedrock" and "application-inference-profile" in endpoint:
        encoded_url_str = CommonUtils.encode_bedrock_runtime_modelid_arn(
            str(updated_url)
        )
        updated_url = httpx.URL(encoded_url_str)

    # Add or update query parameters
    provider_api_key = provider_config.get_api_key(api_key)

    auth_headers = provider_config.validate_environment(
        headers={},
        model=model,
        messages=[],
        optional_params={},
        litellm_params=litellm_params_dict,
        api_key=provider_api_key,
        api_base=base_target_url,
    )

    headers = BasePassthroughUtils.forward_headers_from_request(
        request_headers=request_headers or {},
        headers=auth_headers,
        forward_headers=False,
    )

    headers, signed_json_body = provider_config.sign_request(
        headers=headers,
        litellm_params=litellm_params_dict,
        request_data=data if data else json,
        api_base=str(updated_url),
        model=model,
    )

    ## SWAP MODEL IN JSON BODY [TODO: REFACTOR TO A provider_config.transform_request method]
    if json and isinstance(json, dict) and "model" in json:
        json["model"] = model

    request = client.client.build_request(
        method=method,
        url=updated_url,
        content=signed_json_body if signed_json_body is not None else content,
        data=data if (signed_json_body is None and content is None) else None,
        files=files,
        json=json if (signed_json_body is None and content is None) else None,
        params=params,
        headers=headers,
        cookies=cookies,
    )

    ## IS STREAMING REQUEST
    is_streaming_request = provider_config.is_streaming_request(
        endpoint=endpoint,
        request_data=data or json or {},
    )

    # Update logging object with streaming status
    litellm_logging_obj.stream = is_streaming_request

    ## LOGGING PRE-CALL
    request_data = data if data else json
    litellm_logging_obj.pre_call(
        input=request_data,
        api_key=provider_api_key,
        additional_args={
            "complete_input_dict": request_data,
            "api_base": str(updated_url),
            "headers": headers,
        },
    )

    try:
        if _is_async:
            # Return the coroutine to be awaited by the caller
            return _async_passthrough_request(
                client=client,
                request=request,
                is_streaming_request=is_streaming_request,
                litellm_logging_obj=litellm_logging_obj,
                provider_config=provider_config,
            )
        else:
            # Sync path - client.client.send returns Response directly
            response: httpx.Response = client.client.send(request=request, stream=is_streaming_request)  # type: ignore
            response.raise_for_status()

            if (
                hasattr(response, "iter_bytes") and is_streaming_request
            ):  # yield the chunk, so we can store it in the logging object
                return _sync_streaming(response, litellm_logging_obj, provider_config)
            else:
                # For non-streaming responses, yield the entire response
                return response
    except Exception as e:
        if provider_config is None:
            raise e
        raise base_llm_http_handler._handle_error(
            e=e,
            provider_config=provider_config,
        )

