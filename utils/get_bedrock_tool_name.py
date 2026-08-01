
def get_bedrock_tool_name(response_tool_name: str) -> str:
    """
    If litellm formatted the input tool name, we need to convert it back to the original name.

    Args:
        response_tool_name (str): The name of the tool as received from the response.

    Returns:
        str: The original name of the tool.
    """

    if response_tool_name in litellm.bedrock_tool_name_mappings.cache_dict:
        response_tool_name = litellm.bedrock_tool_name_mappings.cache_dict[
            response_tool_name
        ]
    return response_tool_name

