
def token_counter(
    model="",
    custom_tokenizer: Optional[Union[dict, SelectTokenizerResponse]] = None,
    text: Optional[Union[str, List[str]]] = None,
    messages: Optional[List] = None,
    count_response_tokens: Optional[bool] = False,
    tools: Optional[List[ChatCompletionToolParam]] = None,
    tool_choice: Optional[ChatCompletionNamedToolChoiceParam] = None,
    use_default_image_token_count: Optional[bool] = False,
    default_token_count: Optional[int] = None,
) -> int:
    """
    The same as `litellm.litellm_core_utils.token_counter`.

    Kept for backwards compatibility.
    """

    #########################################################
    # Flag to disable token counter
    # We've gotten reports of this consuming CPU cycles,
    # exposing this flag to allow users to disable
    # it to confirm if this is indeed the issue
    #########################################################
    if litellm.disable_token_counter is True:
        return 0

    return _get_token_counter_new()(
        model,
        custom_tokenizer,
        text,
        messages,
        count_response_tokens,
        tools,
        tool_choice,
        use_default_image_token_count,
        default_token_count,
    )


def token_counter(
    model="",
    custom_tokenizer: Optional[Union[dict, SelectTokenizerResponse]] = None,
    text: Optional[Union[str, List[str]]] = None,
    messages: Optional[List[Union[AllMessageValues, Message]]] = None,
    count_response_tokens: Optional[bool] = False,
    tools: Optional[List[ChatCompletionToolParam]] = None,
    tool_choice: Optional[ChatCompletionNamedToolChoiceParam] = None,
    use_default_image_token_count: Optional[bool] = False,
    default_token_count: Optional[int] = None,
) -> int:
    """
    Count the number of tokens in a given text using a specified model.

    Args:
    model (str): The name of the model to use for tokenization. Default is an empty string.
    custom_tokenizer (Optional[dict]): A custom tokenizer created with the `create_pretrained_tokenizer` or `create_tokenizer` method. Must be a dictionary with a string value for `type` and Tokenizer for `tokenizer`. Default is None.
    text (str): The raw text string to be passed to the model. Default is None.
    messages (Optional[List[AllMessageValues]]): Alternative to passing in text. A list of dictionaries representing messages with "role" and "content" keys. Default is None.
    count_response_tokens (Optional[bool]): set to True to indicate we are processing a stream response.
    tools (Optional[List[ChatCompletionToolParam]]): The available tools. Default is None.
    tool_choice (Optional[ChatCompletionNamedToolChoiceParam]): The tool choice. Default is None.
    use_default_image_token_count (Optional[bool]): When True, will NOT make a GET request to the image URL and instead return the default image dimensions. Default is False.
    default_token_count (Optional[int]): The default number of tokens to return for a message block, if an error occurs. Default is None.

    Returns:
    int: The number of tokens in the text.
    """
    from litellm.utils import convert_list_message_to_dict

    #########################################################
    # Flag to disable token counter
    # We've gotten reports of this consuming CPU cycles,
    # exposing this flag to allow users to disable
    # it to confirm if this is indeed the issue
    #########################################################
    if litellm.disable_token_counter is True:
        return 0

    verbose_logger.debug(
        f"messages in token_counter: {messages}, text in token_counter: {text}"
    )
    if text is not None and messages is not None:
        raise ValueError("text and messages cannot both be set")
    if use_default_image_token_count is None:
        use_default_image_token_count = False

    if text is not None:
        if tools or tool_choice:
            raise ValueError("tools or tool_choice cannot be set if using text")
        if isinstance(text, List):
            text_to_count = "".join(t for t in text if isinstance(t, str))
        elif isinstance(text, str):
            text_to_count = text
        count_function = _get_count_function(model, custom_tokenizer)
        num_tokens = count_function(text_to_count)

    elif messages is not None:
        new_messages = cast(
            List[AllMessageValues], convert_list_message_to_dict(messages)
        )
        params = _MessageCountParams(model, custom_tokenizer)
        num_tokens = _count_messages(
            params, new_messages, use_default_image_token_count, default_token_count
        )
        if count_response_tokens is False:
            includes_system_message = any(
                [message.get("role", None) == "system" for message in new_messages]
            )
            num_tokens += _count_extra(
                params.count_function, tools, tool_choice, includes_system_message
            )

    else:
        raise ValueError("Either text or messages must be provided")

    return num_tokens

