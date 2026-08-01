
def get_skill(
    skill_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[Skill, Coroutine[Any, Any, Skill]]:
    """
    Get a skill by ID

    Args:
        skill_id: The ID of the skill to fetch
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        timeout: Request timeout
        custom_llm_provider: Provider name (e.g., 'anthropic')
        **kwargs: Additional parameters

    Returns:
        Skill object
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aget_skill", False) is True

        # Get LiteLLM parameters
        litellm_params = GenericLiteLLMParams(**kwargs)

        # Determine provider
        if custom_llm_provider is None:
            custom_llm_provider = "anthropic"

        # Route to LiteLLM DB if custom_llm_provider="litellm_proxy"
        if custom_llm_provider == LlmProviders.LITELLM_PROXY.value:
            return _get_litellm_skills_handler().get_skill_handler(
                skill_id=skill_id,
                user_api_key_dict=_get_user_api_key_auth_from_kwargs(kwargs),
                _is_async=_is_async,
                logging_obj=litellm_logging_obj,
                litellm_call_id=litellm_call_id,
            )

        # Get provider config for external providers (Anthropic, etc.)
        skills_api_provider_config: Optional[BaseSkillsAPIConfig] = (
            ProviderConfigManager.get_provider_skills_api_config(
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if skills_api_provider_config is None:
            raise ValueError(f"GET skill is not supported for {custom_llm_provider}")

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = skills_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Get API base
        from litellm.llms.anthropic.common_utils import AnthropicModelInfo

        api_base = AnthropicModelInfo.get_api_base(litellm_params.api_base)

        # Transform request
        url, headers = skills_api_provider_config.transform_get_skill_request(
            skill_id=skill_id,
            api_base=api_base or DEFAULT_ANTHROPIC_API_BASE,
            litellm_params=litellm_params,
            headers=headers,
        )

        # Pre-call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"skill_id": skill_id},
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Make HTTP request
        response = base_llm_http_handler.get_skill_handler(
            url=url,
            skills_api_provider_config=skills_api_provider_config,
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

