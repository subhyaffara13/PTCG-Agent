
def _lazy_import_http_handlers(name: str) -> Any:
    """
    Handler for HTTP clients - has special logic for creating client instances.

    This one is different because:
    - These aren't just imports, they're actual client instances that need to be created
    - They need configuration (timeout, etc.) from the module globals
    - They use factory functions instead of direct instantiation
    """
    _globals = _get_litellm_globals()

    if name == "module_level_aclient":
        # Create an async HTTP client using the factory function
        from litellm.llms.custom_httpx.http_handler import get_async_httpx_client

        # Get timeout from module config (if set)
        timeout = _globals.get("request_timeout")
        params = {"timeout": timeout, "client_alias": "module level aclient"}

        # Create the client instance
        provider_id = cast(Any, "litellm_module_level_client")
        async_client = get_async_httpx_client(
            llm_provider=provider_id,
            params=params,
        )

        # Cache it so we don't create it again
        _globals["module_level_aclient"] = async_client
        return async_client

    if name == "module_level_client":
        # Create a sync HTTP client
        from litellm.llms.custom_httpx.http_handler import HTTPHandler

        timeout = _globals.get("request_timeout")
        sync_client = HTTPHandler(timeout=timeout)

        # Cache it
        _globals["module_level_client"] = sync_client
        return sync_client

    raise AttributeError(f"HTTP handlers lazy import: unknown attribute {name!r}")

