import json
from typing import List

def _convert_to_bedrock_tool_call_invoke(
    tool_calls: list,
) -> List[BedrockContentBlock]:
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
    Bedrock tool invokes: 
    [   
        {
            "role": "assistant",
            "toolUse": {
                "input": {"location": "Boston, MA", ..},
                "name": "get_current_weather",
                "toolUseId": "call_abc123"
            }
        }
    ]
    """
    """
    - json.loads argument
    - extract name 
    - extract id
    """
    from litellm.litellm_core_utils.prompt_templates.common_utils import (
        split_concatenated_json_objects,
    )

    try:
        _parts_list: List[BedrockContentBlock] = []
        for tool in tool_calls:
            if "function" in tool:
                tool_id = tool["id"]
                name = make_valid_bedrock_tool_name(tool["function"].get("name", ""))
                arguments = tool["function"].get("arguments", "")

                if not arguments or not arguments.strip():
                    arguments_dict = {}
                else:
                    try:
                        arguments_dict = json.loads(arguments)
                        # Ensure arguments_dict is always a dict
                        # (Bedrock requires toolUse.input to be an object).
                        # Some providers return arguments: '""' which
                        # json.loads decodes to a bare string.
                        if not isinstance(arguments_dict, dict):
                            arguments_dict = {}
                    except json.JSONDecodeError:
                        # The model may return multiple JSON objects
                        # concatenated in a single arguments string, e.g.
                        #   '{"cmd":"a"}{"cmd":"b"}{"cmd":"c"}'
                        # Split them and emit one toolUse block per object.
                        # Fixes: https://github.com/BerriAI/litellm/issues/20543
                        parsed_objects = split_concatenated_json_objects(arguments)
                        if parsed_objects:
                            # First object keeps the original tool id.
                            for obj_idx, obj in enumerate(parsed_objects):
                                block_id = (
                                    tool_id if obj_idx == 0 else f"{tool_id}_{obj_idx}"
                                )
                                bedrock_tool = BedrockToolUseBlock(
                                    input=obj, name=name, toolUseId=block_id
                                )
                                _parts_list.append(
                                    BedrockContentBlock(toolUse=bedrock_tool)
                                )
                            # cache_control applies to the whole original
                            # tool call; attach after the last split block.
                            if tool.get("cache_control", None) is not None:
                                _parts_list.append(
                                    BedrockContentBlock(
                                        cachePoint=CachePointBlock(type="default")
                                    )
                                )
                            continue
                        # Fallback: no objects extracted — use empty dict.
                        arguments_dict = {}

                bedrock_tool = BedrockToolUseBlock(
                    input=arguments_dict, name=name, toolUseId=tool_id
                )
                bedrock_content_block = BedrockContentBlock(toolUse=bedrock_tool)
                _parts_list.append(bedrock_content_block)

                # Check for cache_control and add a separate cachePoint block
                if tool.get("cache_control", None) is not None:
                    cache_point_block = BedrockContentBlock(
                        cachePoint=CachePointBlock(type="default")
                    )
                    _parts_list.append(cache_point_block)
        return _parts_list
    except Exception as e:
        raise Exception(
            "Unable to convert openai tool calls={} to bedrock tool calls. Received error={}".format(
                tool_calls, str(e)
            )
        )

