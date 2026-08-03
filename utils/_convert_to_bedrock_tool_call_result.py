import uuid
from typing import Union

def _convert_to_bedrock_tool_call_result(
    message: Union[ChatCompletionToolMessage, ChatCompletionFunctionMessage],
) -> BedrockContentBlock:
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
    Bedrock result looks like this: 
    {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": "tooluse_kZJMlvQmRJ6eAyJE5GIl7Q",
                    "content": [
                        {
                            "json": {
                                "song": "Elemental Hotel",
                                "artist": "8 Storey Hike"
                            }
                        }
                    ]
                }
            }
        ]
    }
    """
    """
    - 
    """
    tool_result_content_blocks, used_search_results = (
        _build_bedrock_tool_result_content_blocks(message)
    )

    message.get("name", "")
    id = str(message.get("tool_call_id", str(uuid.uuid4())))

    tool_result = BedrockToolResultBlock(
        content=tool_result_content_blocks, toolUseId=id
    )
    if used_search_results:
        tool_result["status"] = cast(Literal["success"], "success")

    content_block = BedrockContentBlock(toolResult=tool_result)

    return content_block

