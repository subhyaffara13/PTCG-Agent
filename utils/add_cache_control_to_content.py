
def add_cache_control_to_content(
    anthropic_content_element: Union[
        dict,
        AnthropicMessagesImageParam,
        AnthropicMessagesTextParam,
        AnthropicMessagesDocumentParam,
        AnthropicMessagesToolUseParam,
        ChatCompletionThinkingBlock,
    ],
    original_content_element: Union[dict, AllMessageValues],
):
    cache_control_param = original_content_element.get("cache_control")
    if cache_control_param is not None and isinstance(cache_control_param, dict):
        transformed_param = ChatCompletionCachedContent(**cache_control_param)  # type: ignore

        anthropic_content_element["cache_control"] = transformed_param

    return anthropic_content_element

