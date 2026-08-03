from typing import List, Optional, Union

def sync_transform_request_body(
    gemini_api_key: Optional[str],
    messages: List[AllMessageValues],
    api_base: Optional[str],
    model: str,
    client: Optional[HTTPHandler],
    timeout: Optional[Union[float, httpx.Timeout]],
    extra_headers: Optional[dict],
    optional_params: dict,
    logging_obj: LiteLLMLoggingObj,
    custom_llm_provider: Literal["vertex_ai", "vertex_ai_beta", "gemini"],
    litellm_params: dict,
    vertex_project: Optional[str],
    vertex_location: Optional[str],
    vertex_auth_header: Optional[str],
) -> RequestBody:
    from ..context_caching.vertex_ai_context_caching import ContextCachingEndpoints

    context_caching_endpoints = ContextCachingEndpoints()

    (
        messages,
        optional_params,
        cached_content,
    ) = context_caching_endpoints.check_and_create_cache(
        messages=messages,
        optional_params=optional_params,
        api_key=gemini_api_key or "dummy",
        api_base=api_base,
        model=model,
        client=client,
        timeout=timeout,
        extra_headers=extra_headers,
        cached_content=optional_params.pop("cached_content", None),
        logging_obj=logging_obj,
        custom_llm_provider=custom_llm_provider,
        vertex_project=vertex_project,
        vertex_location=vertex_location,
        vertex_auth_header=vertex_auth_header,
    )

    return _transform_request_body(
        messages=messages,
        model=model,
        custom_llm_provider=custom_llm_provider,
        litellm_params=litellm_params,
        cached_content=cached_content,
        optional_params=optional_params,
    )

