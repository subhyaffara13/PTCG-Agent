
def _responses_try_dispatch_emulated_file_search(
    *,
    tools: Optional[Iterable[ToolParam]],
    input: Union[str, ResponseInputParam],
    model: str,
    responses_api_provider_config: Optional[BaseResponsesAPIConfig],
    use_chat_completions_api: bool,
    include: Optional[List[ResponseIncludable]],
    instructions: Optional[str],
    max_output_tokens: Optional[int],
    prompt: Optional[PromptObject],
    metadata: Optional[Dict[str, Any]],
    parallel_tool_calls: Optional[bool],
    previous_response_id: Optional[str],
    reasoning: Optional[Reasoning],
    store: Optional[bool],
    background: Optional[bool],
    stream: Optional[bool],
    temperature: Optional[float],
    text: Any,
    tool_choice: Optional[ToolChoice],
    top_p: Optional[float],
    truncation: Optional[Literal["auto", "disabled"]],
    user: Optional[str],
    service_tier: Optional[str],
    safety_identifier: Optional[str],
    text_format: Optional[Union[Type[BaseModel], dict]],
    allowed_openai_params: Optional[List[str]],
    extra_headers: Optional[Dict[str, Any]],
    extra_query: Optional[Dict[str, Any]],
    extra_body: Optional[Dict[str, Any]],
    timeout: Optional[Union[float, httpx.Timeout]],
    custom_llm_provider: Optional[str],
    kwargs: Dict[str, Any],
    _is_async: bool,
) -> Optional[Any]:
    """Return a response when emulated file_search handles the call; otherwise None."""
    if not _has_file_search_tool(tools) or not (
        responses_api_provider_config is None
        or use_chat_completions_api is True
        or not responses_api_provider_config.supports_native_file_search()
    ):
        return None
    from litellm.responses.file_search.emulated_handler import (
        aresponses_with_emulated_file_search,
    )

    _internal_skip = {"litellm_call_id", "aresponses"}
    emulated_kwargs = {
        "include": include,
        "instructions": instructions,
        "max_output_tokens": max_output_tokens,
        "prompt": prompt,
        "metadata": metadata,
        "parallel_tool_calls": parallel_tool_calls,
        "previous_response_id": previous_response_id,
        "reasoning": reasoning,
        "store": store,
        "background": background,
        "stream": stream,
        "temperature": temperature,
        "text": text,
        "tool_choice": tool_choice,
        "top_p": top_p,
        "truncation": truncation,
        "user": user,
        "service_tier": service_tier,
        "safety_identifier": safety_identifier,
        "text_format": text_format,
        "allowed_openai_params": allowed_openai_params,
        "extra_headers": extra_headers,
        "extra_query": extra_query,
        "extra_body": extra_body,
        "timeout": timeout,
        "custom_llm_provider": custom_llm_provider,
        **(
            {
                **(
                    {"use_chat_completions_api": True}
                    if use_chat_completions_api
                    else {}
                ),
                **{k: v for k, v in kwargs.items() if k not in _internal_skip},
            }
        ),
    }
    if _is_async:
        return aresponses_with_emulated_file_search(
            input=input, model=model, tools=tools, **emulated_kwargs
        )
    return run_async_function(
        aresponses_with_emulated_file_search,
        input=input,
        model=model,
        tools=tools,
        **emulated_kwargs,
    )

