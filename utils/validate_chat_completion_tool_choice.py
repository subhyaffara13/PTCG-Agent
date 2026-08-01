
def validate_chat_completion_tool_choice(
    tool_choice: Optional[Union[dict, str]],
) -> Optional[Union[dict, str]]:
    """
    Confirm the tool choice is passed in the OpenAI format.

    Prevents user errors like: https://github.com/BerriAI/litellm/issues/7483
    """
    from litellm.types.llms.openai import (
        ChatCompletionToolChoiceObjectParam,
        ChatCompletionToolChoiceStringValues,
    )

    if tool_choice is None:
        return tool_choice
    elif isinstance(tool_choice, str):
        return tool_choice
    elif isinstance(tool_choice, dict):
        # Handle Cursor IDE format: {"type": "auto"} -> return as-is
        if (
            tool_choice.get("type") in ["auto", "none", "required"]
            and "function" not in tool_choice
        ):
            return tool_choice

        # Standard OpenAI format: {"type": "function", "function": {...}}
        if tool_choice.get("type") is None or tool_choice.get("function") is None:
            raise Exception(
                f"Invalid tool choice, tool_choice={tool_choice}. Please ensure tool_choice follows the OpenAI spec"
            )
        return tool_choice
    raise Exception(
        f"Invalid tool choice, tool_choice={tool_choice}. Got={type(tool_choice)}. Expecting str, or dict. Please ensure tool_choice follows the OpenAI tool_choice spec"
    )

