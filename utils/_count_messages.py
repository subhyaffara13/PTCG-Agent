from typing import List, Optional

def _count_messages(
    params: _MessageCountParams,
    messages: List[AllMessageValues],
    use_default_image_token_count: bool,
    default_token_count: Optional[int],
) -> int:
    """
    Count the number of tokens in a list of messages.

    Args:
        params (_MessageCountParams): The parameters for counting tokens.
        messages (List[AllMessageValues]): The list of messages to count tokens in.
        use_default_image_token_count (bool): When True, will NOT make a GET request to the image URL and instead return the default image dimensions.
        default_token_count (Optional[int]): The default number of tokens to return for a message block, if an error occurs.
    """
    num_tokens = 0
    if len(messages) == 0:
        return num_tokens
    for message in messages:
        num_tokens += params.tokens_per_message
        for key, value in message.items():
            if value is None:
                pass
            elif key == "tool_calls":
                if isinstance(value, List):
                    for tool_call in value:
                        if "function" in tool_call:
                            function_arguments = tool_call["function"].get(
                                "arguments", []
                            )
                            num_tokens += params.count_function(str(function_arguments))
                        else:
                            raise ValueError(
                                f"Unsupported tool call {tool_call} must contain a function key"
                            )
                else:
                    raise ValueError(
                        f"Unsupported type {type(value)} for key tool_calls in message {message}"
                    )
            elif isinstance(value, str):
                num_tokens += params.count_function(value)
                if key == "name":
                    num_tokens += params.tokens_per_name
            elif key == "content" and isinstance(value, List):
                num_tokens += _count_content_list(
                    params.count_function,
                    value,
                    use_default_image_token_count,
                    default_token_count,
                )
            elif key == "search_results" and isinstance(value, list):
                from litellm.litellm_core_utils.prompt_templates.common_utils import (
                    extract_search_results_text,
                )

                search_results_text = extract_search_results_text(value)
                if search_results_text:
                    num_tokens += params.count_function(search_results_text)
            else:
                # Skip unsupported keys instead of raising an error
                continue
    return num_tokens

