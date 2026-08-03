from typing import Any, Dict, List, Optional, Union

def _responses_try_dispatch_mcp_gateway(
    *,
    tools: Optional[Iterable[ToolParam]],
    input: Union[str, ResponseInputParam],
    model: str,
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
    extra_headers: Optional[Dict[str, Any]],
    extra_query: Optional[Dict[str, Any]],
    extra_body: Optional[Dict[str, Any]],
    timeout: Optional[Union[float, httpx.Timeout]],
    custom_llm_provider: Optional[str],
    kwargs: Dict[str, Any],
    _is_async: bool,
) -> Optional[Any]:
    """Return a response when MCP gateway handles the call; otherwise None."""
    from litellm.responses.mcp.litellm_proxy_mcp_handler import (
        LiteLLM_Proxy_MCP_Handler,
    )

    if not LiteLLM_Proxy_MCP_Handler._should_use_litellm_mcp_gateway(tools=tools):
        return None
    mcp_call_kwargs = {
        "input": input,
        "model": model,
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
        "tools": tools,
        "top_p": top_p,
        "truncation": truncation,
        "user": user,
        "extra_headers": extra_headers,
        "extra_query": extra_query,
        "extra_body": extra_body,
        "timeout": timeout,
        "custom_llm_provider": custom_llm_provider,
        **kwargs,
    }
    if _is_async:
        return aresponses_api_with_mcp(**mcp_call_kwargs)
    return run_async_function(aresponses_api_with_mcp, **mcp_call_kwargs)

