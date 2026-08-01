
def create_skill(
    files: Optional[List[Any]] = None,
    display_title: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[Skill, Coroutine[Any, Any, Skill]]:
    """
    Create a new skill

    Args:
        files: Files to upload for the skill. All files must be in the same top-level directory and must include a SKILL.md file at the root.
        display_title: Optional display title for the skill
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        extra_body: Additional body parameters
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
        _is_async = kwargs.pop("acreate_skill", False) is True

        # Get LiteLLM parameters
        litellm_params = GenericLiteLLMParams(**kwargs)

        # Determine provider
        if custom_llm_provider is None:
            custom_llm_provider = "anthropic"

        # Build create request
        create_request: CreateSkillRequest = {}
        if display_title is not None:
            create_request["display_title"] = display_title
        if files is not None:
            create_request["files"] = files

        # Merge extra_body if provided
        if extra_body:
            create_request.update(extra_body)  # type: ignore

        # Route to LiteLLM DB if custom_llm_provider="litellm_proxy"
        if custom_llm_provider == LlmProviders.LITELLM_PROXY.value:
            return _get_litellm_skills_handler().create_skill_handler(
                display_title=display_title,
                files=files,
                metadata=_get_skill_request_metadata(kwargs, extra_body),
                user_id=kwargs.get("user_id"),
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
            raise ValueError(f"CREATE skill is not supported for {custom_llm_provider}")

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = skills_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Transform request
        request_body = skills_api_provider_config.transform_create_skill_request(
            create_request=create_request,
            litellm_params=litellm_params,
            headers=headers,
        )

        # Get API base and URL
        from litellm.llms.anthropic.common_utils import AnthropicModelInfo

        api_base = AnthropicModelInfo.get_api_base(litellm_params.api_base)
        url = skills_api_provider_config.get_complete_url(
            api_base=api_base, endpoint="skills"
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
        response = base_llm_http_handler.create_skill_handler(
            url=url,
            request_body=request_body,
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

