
def _count_extra(
    count_function: TokenCounterFunction,
    tools: Optional[List[ChatCompletionToolParam]],
    tool_choice: Optional[ChatCompletionNamedToolChoiceParam],
    includes_system_message: bool,
) -> int:
    """Count extra tokens for function definitions and tool choices.
    Args:
        count_function (TokenCounterFunction): The function to count tokens.
        tools (Optional[List[ChatCompletionToolParam]]): The available tools.
        tool_choice (Optional[ChatCompletionNamedToolChoiceParam]): The tool choice.
        includes_system_message (bool): Whether the messages include a system message.
    """

    num_tokens = 3  # every reply is primed with <|start|>assistant<|message|>

    if tools:
        num_tokens += count_function(_format_function_definitions(tools))
        num_tokens += 9  # Additional tokens for function definition of tools
    # If there's a system message and tools are present, subtract four tokens
    if tools and includes_system_message:
        num_tokens -= 4
    # If tool_choice is 'none', add one token.
    # If it's an object, add 4 + the number of tokens in the function name.
    # If it's undefined or 'auto', don't add anything.
    if tool_choice == "none":
        num_tokens += 1
    elif isinstance(tool_choice, dict):
        num_tokens += 7
        num_tokens += count_function(str(tool_choice["function"]["name"]))

    return num_tokens

