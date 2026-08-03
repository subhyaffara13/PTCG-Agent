import copy
from typing import List, Optional

def _bedrock_tools_pt(
    tools: List, model: Optional[str] = None
) -> List[BedrockToolBlock]:
    """
    OpenAI tools looks like:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        }
    ]
    """
    """
    Bedrock toolConfig looks like:
    "tools": [
        {
            "toolSpec": {
                "name": "top_song",
                "description": "Get the most popular song played on a radio station.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "sign": {
                                "type": "string",
                                "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ, and WKRP."
                            }
                        },
                        "required": [
                            "sign"
                        ]
                    }
                }
            }
        }
    ]
    """
    from litellm.llms.bedrock.common_utils import (
        get_bedrock_base_model,
        normalize_json_schema_custom_types_to_object,
    )
    from litellm.litellm_core_utils.prompt_templates.common_utils import unpack_defs

    _valid_json_schema_root_types = frozenset(
        ("array", "boolean", "integer", "null", "number", "object", "string")
    )
    # Only Claude on Bedrock honours strict tool schemas; other families
    # (Nova, Llama, GPT-OSS) reject the strict field outright.
    supports_strict_tools = bool(
        model and get_bedrock_base_model(model).startswith("anthropic")
    )
    tool_block_list: List[BedrockToolBlock] = []
    for tool_idx, tool in enumerate(tools):
        # Check if tool is already a BedrockToolBlock (e.g., systemTool for Nova grounding)
        if _is_bedrock_tool_block(tool):
            # Already a BedrockToolBlock, pass it through
            tool_block_list.append(tool)  # type: ignore
            continue

        # OpenAI function tools, or Anthropic Messages / Claude Code ({name, input_schema, type, ...})
        if isinstance(tool, dict) and "input_schema" in tool and "function" not in tool:
            parameters = copy.deepcopy(
                tool.get("input_schema") or {"type": "object", "properties": {}}
            )
            raw_name = tool.get("name", "") or ""
            _tool_description = tool.get("description", None)
        else:
            parameters = copy.deepcopy(
                tool.get("function", {}).get(
                    "parameters", {"type": "object", "properties": {}}
                )
            )
            raw_name = tool.get("function", {}).get("name", "") or ""
            _tool_description = tool.get("function", {}).get("description", None)

        if not (raw_name and str(raw_name).strip()):
            raw_name = f"litellm_unnamed_tool_{tool_idx}"

        # related issue: https://github.com/BerriAI/litellm/issues/5007
        # Bedrock tool names must satisfy pattern: [a-zA-Z][a-zA-Z0-9_-]*
        name = make_valid_bedrock_tool_name(input_tool_name=raw_name)
        if _tool_description:  # bedrock doesn't accept empty "" or None descriptions
            description = _tool_description
        else:
            description = name

        defs = parameters.pop("$defs", {})
        defs_copy = copy.deepcopy(defs)
        # Expand $ref references in parameters using the definitions
        # Note: We don't pre-flatten defs as that causes exponential memory growth
        # with circular references (see issue #19098). unpack_defs handles nested
        # refs recursively and correctly detects/skips circular references.
        unpack_defs(parameters, defs_copy)
        normalize_json_schema_custom_types_to_object(parameters)
        if parameters.get("type") not in _valid_json_schema_root_types:
            parameters["type"] = "object"
        tool_block = cast(
            BedrockToolBlock,
            BedrockToolSpec(
                name=name,
                description=description,
                parameters=parameters,
                strict=tool.get("function", {}).get("strict", None),
                supports_strict_tools=supports_strict_tools,
            ),
        )
        tool_block_list.append(tool_block)

        ## ADD CACHE POINT TOOL BLOCK ##
        cache_point_tool_block = add_cache_point_tool_block(tool, model=model)
        if cache_point_tool_block is not None:
            tool_block_list.append(cache_point_tool_block)

    return tool_block_list

