
def convert_to_anthropic_tool_result(
    message: Union[ChatCompletionToolMessage, ChatCompletionFunctionMessage],
    force_base64: bool = False,
) -> AnthropicMessagesToolResultParam:
    """
    OpenAI message with a tool result looks like:
    {
        "tool_call_id": "tool_1",
        "role": "tool",
        "name": "get_current_weather",
        "content": "function result goes here",
    },

    OpenAI message with a function call result looks like:
    {
        "role": "function",
        "name": "get_current_weather",
        "content": "function result goes here",
    }
    """

    """
    Anthropic tool_results look like:
    {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
                "content": "ConnectionError: the weather service API is not available (HTTP 500)",
                # "is_error": true
            }
        ]
    }
    """
    anthropic_content: Union[
        str,
        List[
            Union[
                AnthropicMessagesToolResultContent,
                AnthropicMessagesImageParam,
                AnthropicMessagesDocumentParam,
            ]
        ],
    ] = ""
    if isinstance(message["content"], str):
        anthropic_content = message["content"]
    elif isinstance(message["content"], List):
        content_list = message["content"]
        anthropic_content_list: List[
            Union[
                AnthropicMessagesToolResultContent,
                AnthropicMessagesImageParam,
                AnthropicMessagesDocumentParam,
            ]
        ] = []
        for content in content_list:
            if content["type"] == "text":
                # Only include cache_control if explicitly set and not None
                # to avoid sending "cache_control": null which breaks some API channels
                text_content: AnthropicMessagesToolResultContent = {
                    "type": "text",
                    "text": content["text"],
                }
                cache_control_value = content.get("cache_control")
                if cache_control_value is not None:
                    text_content["cache_control"] = cache_control_value
                anthropic_content_list.append(text_content)
            elif content["type"] == "image_url":
                image_url_value = content["image_url"]
                format = (
                    image_url_value.get("format")
                    if isinstance(image_url_value, dict)
                    else None
                )
                url_str = (
                    image_url_value.get("url")
                    if isinstance(image_url_value, dict)
                    else image_url_value
                )
                # Data URIs with non-image mime types (e.g. application/pdf) must
                # translate to Anthropic document blocks, not image blocks —
                # wrapping a PDF in `type: "image"` is rejected by the API.
                if isinstance(url_str, str) and _is_anthropic_document_data_uri(
                    url_str
                ):
                    synth_file_message: ChatCompletionFileObject = {
                        "type": "file",
                        "file": {"file_data": url_str},
                    }
                    _document_block = anthropic_process_openai_file_message(
                        synth_file_message
                    )
                    _document_block = add_cache_control_to_content(
                        anthropic_content_element=cast(
                            AnthropicMessagesDocumentParam, _document_block
                        ),
                        original_content_element=content,
                    )
                    anthropic_content_list.append(
                        cast(AnthropicMessagesDocumentParam, _document_block)
                    )
                else:
                    _anthropic_image_param = create_anthropic_image_param(
                        image_url_value,
                        format=format,
                        is_bedrock_invoke=force_base64,
                    )
                    _anthropic_image_param = add_cache_control_to_content(
                        anthropic_content_element=_anthropic_image_param,
                        original_content_element=content,
                    )
                    anthropic_content_list.append(
                        cast(AnthropicMessagesImageParam, _anthropic_image_param)
                    )
            elif content["type"] == "file":
                file_content = cast(ChatCompletionFileObject, content)
                _file_block = anthropic_process_openai_file_message(file_content)
                _file_block = add_cache_control_to_content(
                    anthropic_content_element=cast(
                        AnthropicMessagesDocumentParam, _file_block
                    ),
                    original_content_element=content,
                )
                anthropic_content_list.append(_file_block)

        anthropic_content = anthropic_content_list
    anthropic_tool_result: Optional[AnthropicMessagesToolResultParam] = None
    ## PROMPT CACHING CHECK ##
    cache_control = message.get("cache_control", None)
    if message["role"] == "tool":
        tool_message: ChatCompletionToolMessage = message
        tool_call_id: str = tool_message["tool_call_id"]
        # Sanitize tool_use_id to match Anthropic's pattern requirement: ^[a-zA-Z0-9_-]+$
        sanitized_tool_use_id = _sanitize_anthropic_tool_use_id(tool_call_id)

        # We can't determine from openai message format whether it's a successful or
        # error call result so default to the successful result template
        anthropic_tool_result = AnthropicMessagesToolResultParam(
            type="tool_result",
            tool_use_id=sanitized_tool_use_id,
            content=anthropic_content,
        )

    if message["role"] == "function":
        function_message: ChatCompletionFunctionMessage = message
        tool_call_id = function_message.get("tool_call_id") or str(uuid.uuid4())
        # Sanitize tool_use_id to match Anthropic's pattern requirement: ^[a-zA-Z0-9_-]+$
        sanitized_tool_use_id = _sanitize_anthropic_tool_use_id(tool_call_id)
        anthropic_tool_result = AnthropicMessagesToolResultParam(
            type="tool_result",
            tool_use_id=sanitized_tool_use_id,
            content=anthropic_content,
        )

    if anthropic_tool_result is None:
        raise Exception(f"Unable to parse anthropic tool result for message: {message}")
    if cache_control is not None:
        anthropic_tool_result["cache_control"] = cache_control  # type: ignore
    return anthropic_tool_result

