
def construct_tool_use_system_prompt(
    tools,
):  # from https://github.com/anthropics/anthropic-cookbook/blob/main/function_calling/function_calling.ipynb
    tool_str_list = []
    for tool in tools:
        tool_function = get_attribute_or_key(tool, "function")
        tool_str = construct_format_tool_for_claude_prompt(
            get_attribute_or_key(tool_function, "name"),
            get_attribute_or_key(tool_function, "description", ""),
            get_attribute_or_key(tool_function, "parameters", {}),
        )
        tool_str_list.append(tool_str)
    tool_use_system_prompt = (
        "In this environment you have access to a set of tools you can use to answer the user's question.\n"
        "\n"
        "You may call them like this:\n"
        "<function_calls>\n"
        "<invoke>\n"
        "<tool_name>$TOOL_NAME</tool_name>\n"
        "<parameters>\n"
        "<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>\n"
        "...\n"
        "</parameters>\n"
        "</invoke>\n"
        "</function_calls>\n"
        "\n"
        "Here are the tools available:\n"
        "<tools>\n" + "\n".join([tool_str for tool_str in tool_str_list]) + "\n</tools>"
    )
    return tool_use_system_prompt

