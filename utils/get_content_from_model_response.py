from typing import Union

def get_content_from_model_response(response: Union[ModelResponse, dict]) -> str:
    """
    Gets content from model response
    """
    if isinstance(response, dict):
        new_response = ModelResponse(**response)
    else:
        new_response = response

    content = ""

    for choice in new_response.choices:
        if isinstance(choice, Choices):
            content += choice.message.content if choice.message.content else ""
            if choice.message.function_call:
                content += choice.message.function_call.model_dump_json()
            if choice.message.tool_calls:
                for tc in choice.message.tool_calls:
                    content += tc.model_dump_json()
        elif isinstance(choice, StreamingChoices):
            content += getattr(choice, "delta", {}).get("content", "") or ""
    return content

