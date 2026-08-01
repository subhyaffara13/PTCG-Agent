
def create_sync_endpoint_function(endpoint_config: Dict) -> Callable:
    """
    Create a sync SDK function from endpoint config.

    Uses the generic container handler instead of individual handler methods.
    """
    endpoint_name = endpoint_config["name"]
    response_type = RESPONSE_TYPES.get(endpoint_config["response_type"])
    path_params = endpoint_config.get("path_params", [])

    @client
    def endpoint_func(
        timeout: int = 600,
        custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
        extra_headers: Optional[Dict[str, Any]] = None,
        extra_query: Optional[Dict[str, Any]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        local_vars = locals()
        try:
            resolved_custom_llm_provider: str = custom_llm_provider
            litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")
            litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
            _is_async = kwargs.pop("async_call", False) is True

            # Check for mock response
            mock_response = kwargs.get("mock_response")
            if mock_response is not None:
                if isinstance(mock_response, str):
                    mock_response = json.loads(mock_response)
                if response_type:
                    return response_type(**mock_response)
                return mock_response

            # Get provider config
            litellm_params = GenericLiteLLMParams(**kwargs)
            # Strip LiteLLM-managed container IDs before calling the provider API
            # (OpenAI enforces max length 64 on container_id).
            if "container_id" in kwargs and isinstance(kwargs["container_id"], str):
                (
                    kwargs["container_id"],
                    resolved_custom_llm_provider,
                    litellm_params,
                ) = decode_managed_container_id_for_request(
                    container_id=kwargs["container_id"],
                    custom_llm_provider=resolved_custom_llm_provider,
                    litellm_params=litellm_params,
                )
            container_provider_config: Optional[BaseContainerConfig] = (
                ProviderConfigManager.get_provider_container_config(
                    provider=litellm.LlmProviders(resolved_custom_llm_provider),
                )
            )

            if container_provider_config is None:
                raise ValueError(
                    f"Container provider config not found for: {resolved_custom_llm_provider}"
                )

            # Build optional params for logging
            optional_params = {k: kwargs.get(k) for k in path_params if k in kwargs}

            # Pre-call logging
            litellm_logging_obj.update_from_kwargs(
                kwargs=kwargs,
                model="",
                optional_params=optional_params,
                litellm_params={"litellm_call_id": litellm_call_id},
                custom_llm_provider=resolved_custom_llm_provider,
            )

            # Use generic handler
            return generic_container_handler.handle(
                endpoint_name=endpoint_name,
                container_provider_config=container_provider_config,
                litellm_params=litellm_params,
                logging_obj=litellm_logging_obj,
                extra_headers=extra_headers,
                extra_query=extra_query,
                timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
                _is_async=_is_async,
                **kwargs,
            )

        except Exception as e:
            raise litellm.exception_type(
                model="",
                custom_llm_provider=resolved_custom_llm_provider,
                original_exception=e,
                completion_kwargs=local_vars,
                extra_kwargs=kwargs,
            )

    return endpoint_func

