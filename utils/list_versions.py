from typing import Any, Dict, Optional, Union

def list_versions(
    name: str,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    **kwargs,
) -> Union[AgentVersionsResponse, Coroutine[Any, Any, AgentVersionsResponse]]:
    """Sync: List versions of a specific agent."""
    local_vars = locals()
    custom_llm_provider = (
        custom_llm_provider or kwargs.get("custom_llm_provider") or "gemini"
    )
    try:
        _is_async = kwargs.pop("alist_agent_versions", False) is True
        kwargs.setdefault("custom_llm_provider", custom_llm_provider)
        litellm_params = GenericLiteLLMParams(**kwargs)
        logging_obj = _make_logging_obj(
            kwargs, name, custom_llm_provider, "list_agent_versions", {"name": name}
        )
        config = _get_agents_api_config(custom_llm_provider)
        return agents_http_handler.list_agent_versions(
            agents_api_config=config,
            name=name,
            litellm_params=litellm_params,
            logging_obj=logging_obj,
            extra_headers=extra_headers,
            timeout=timeout,
            _is_async=_is_async,
        )
    except Exception as e:
        raise litellm.exception_type(
            model=name,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

