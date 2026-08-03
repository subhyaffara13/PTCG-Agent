from typing import Any, Dict, Optional, Union

def update_eval(
    eval_id: str,
    name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[Eval, Coroutine[Any, Any, Eval]]:
    """
    Update an evaluation

    Args:
        eval_id: The ID of the evaluation to update
        name: Updated name
        metadata: Updated metadata
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        extra_body: Additional body parameters
        timeout: Request timeout
        custom_llm_provider: Provider name (e.g., 'openai')
        **kwargs: Additional parameters

    Returns:
        Eval object
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aupdate_eval", False) is True

        # Get LiteLLM parameters
        litellm_params = GenericLiteLLMParams(**kwargs)

        # Determine provider
        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        # Get provider config
        evals_api_provider_config: Optional[BaseEvalsAPIConfig] = (
            ProviderConfigManager.get_provider_evals_api_config(  # type: ignore
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if evals_api_provider_config is None:
            raise ValueError(f"UPDATE eval is not supported for {custom_llm_provider}")

        # Build update request
        update_request: UpdateEvalRequest = {}
        if name is not None:
            update_request["name"] = name

        # Filter metadata to exclude internal LiteLLM fields
        if metadata is not None:
            # List of internal LiteLLM metadata keys that should NOT be sent to OpenAI
            internal_keys = {
                "headers",
                "requester_metadata",
                "user_api_key_hash",
                "user_api_key_alias",
                "user_api_key_spend",
                "user_api_key_max_budget",
                "user_api_key_team_id",
                "user_api_key_user_id",
                "user_api_key_org_id",
                "user_api_key_team_alias",
                "user_api_key_end_user_id",
                "user_api_key_user_email",
                "user_api_key_request_route",
                "user_api_key_budget_reset_at",
                "user_api_key_auth_metadata",
                "user_api_key",
                "user_api_end_user_max_budget",
                "user_api_key_auth",
                "litellm_api_version",
                "global_max_parallel_requests",
                "user_api_key_team_max_budget",
                "user_api_key_team_spend",
                "user_api_key_model_max_budget",
                "user_api_key_user_spend",
                "user_api_key_user_max_budget",
                "user_api_key_metadata",
                "endpoint",
                "litellm_parent_otel_span",
                "requester_ip_address",
                "user_agent",
            }
            # Only include user-provided metadata keys
            filtered_metadata = {
                k: v for k, v in metadata.items() if k not in internal_keys
            }
            if filtered_metadata:  # Only add if there's user metadata
                update_request["metadata"] = filtered_metadata

        # Merge extra_body if provided
        if extra_body:
            update_request.update(extra_body)  # type: ignore

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = evals_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Transform request
        api_base = litellm_params.api_base or DEFAULT_OPENAI_API_BASE
        (
            url,
            headers,
            request_body,
        ) = evals_api_provider_config.transform_update_eval_request(
            eval_id=eval_id,
            update_request=update_request,
            api_base=api_base,
            litellm_params=litellm_params,
            headers=headers,
        )

        # Pre-call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params=request_body,
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Make HTTP request
        response = base_llm_http_handler.update_eval_handler(  # type: ignore
            url=url,
            request_body=request_body,
            evals_api_provider_config=evals_api_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=headers,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
            shared_session=kwargs.get("shared_session"),
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

