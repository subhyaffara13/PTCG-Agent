
def convert_to_anthropic_tool_invoke(
    tool_calls: List[ChatCompletionAssistantToolCall],
    web_search_results: Optional[List[Any]] = None,
    tool_results: Optional[List[Any]] = None,
) -> List[Union[AnthropicMessagesToolUseParam, Dict[str, Any]]]:
    """
    OpenAI tool invokes:
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\n\"location\": \"Boston, MA\"\n}"
          }
        }
      ]
    },
    """

    """
    Anthropic tool invokes:
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "<thinking>To answer this question, I will: 1. Use the get_weather tool to get the current weather in San Francisco. 2. Use the get_time tool to get the current time in the America/Los_Angeles timezone, which covers San Francisco, CA.</thinking>"
        },
        {
          "type": "tool_use",
          "id": "toolu_01A09q90qw90lq917835lq9",
          "name": "get_weather",
          "input": {"location": "San Francisco, CA"}
        }
      ]
    }

    For server-side tools (web_search), we need to reconstruct:
    - server_tool_use blocks (id starts with "srvtoolu_")
    - web_search_tool_result blocks (from provider_specific_fields)

    Fixes: https://github.com/BerriAI/litellm/issues/17737
    """
    anthropic_tool_invoke: List[
        Union[AnthropicMessagesToolUseParam, Dict[str, Any]]
    ] = []

    for tool in tool_calls:
        if not get_attribute_or_key(tool, "type") == "function":
            continue

        tool_id = cast(str, get_attribute_or_key(tool, "id"))
        tool_name = cast(
            str,
            get_attribute_or_key(get_attribute_or_key(tool, "function"), "name"),
        )
        tool_input = parse_tool_call_arguments(
            get_attribute_or_key(get_attribute_or_key(tool, "function"), "arguments"),
            tool_name=tool_name,
            context="Anthropic tool invoke",
        )

        # Check if this is a server-side tool (web_search, tool_search, etc.)
        # Server tool IDs start with "srvtoolu_"
        if tool_id.startswith("srvtoolu_"):
            # Create server_tool_use block instead of tool_use
            _anthropic_server_tool_use: Dict[str, Any] = {
                "type": "server_tool_use",
                "id": tool_id,
                "name": tool_name,
                "input": tool_input,
            }
            anthropic_tool_invoke.append(_anthropic_server_tool_use)

            # Add corresponding tool result if available.
            # Check both web_search_results (web_search_tool_result / web_fetch_tool_result)
            # and tool_results (bash_code_execution_tool_result, etc.)
            _all_tool_results: List[Any] = []
            if web_search_results:
                _all_tool_results.extend(web_search_results)
            if tool_results:
                _all_tool_results.extend(tool_results)
            for result in _all_tool_results:
                if result.get("tool_use_id") == tool_id:
                    anthropic_tool_invoke.append(result)
                    break
        else:
            # Regular tool_use
            sanitized_tool_id = _sanitize_anthropic_tool_use_id(tool_id)
            _anthropic_tool_use_param = AnthropicMessagesToolUseParam(
                type="tool_use",
                id=sanitized_tool_id,
                name=tool_name,
                input=tool_input,
            )

            _content_element = add_cache_control_to_content(
                anthropic_content_element=_anthropic_tool_use_param,
                original_content_element=dict(tool),
            )

            if "cache_control" in _content_element:
                _anthropic_tool_use_param["cache_control"] = _content_element[
                    "cache_control"
                ]

            anthropic_tool_invoke.append(_anthropic_tool_use_param)

    return anthropic_tool_invoke

