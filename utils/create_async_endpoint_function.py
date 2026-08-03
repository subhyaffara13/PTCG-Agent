from typing import Any, Callable, Dict, Optional

def create_async_endpoint_function(
    sync_func: Callable,
    endpoint_config: Dict,
) -> Callable:
    """Create an async SDK function that wraps the sync function."""

    @client
    async def async_endpoint_func(
        timeout: int = 600,
        custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        local_vars = locals()
        try:
            loop = asyncio.get_event_loop()
            kwargs["async_call"] = True

            func = partial(
                sync_func,
                timeout=timeout,
                custom_llm_provider=custom_llm_provider,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                **kwargs,
            )

            ctx = contextvars.copy_context()
            func_with_context = partial(ctx.run, func)
            init_response = await loop.run_in_executor(None, func_with_context)

            if asyncio.iscoroutine(init_response):
                response = await init_response
            else:
                response = init_response

            return response
        except Exception as e:
            raise litellm.exception_type(
                model="",
                custom_llm_provider=custom_llm_provider,
                original_exception=e,
                completion_kwargs=local_vars,
                extra_kwargs=kwargs,
            )

    return async_endpoint_func

