
def convert_to_anthropic_tool_invoke_xml(tool_calls: list) -> str:
    invokes = ""
    for tool in tool_calls:
        if get_attribute_or_key(tool, "type") != "function":
            continue

        tool_function = get_attribute_or_key(tool, "function")
        tool_name = get_attribute_or_key(tool_function, "name")
        tool_arguments = get_attribute_or_key(tool_function, "arguments")
        parsed_args = parse_tool_call_arguments(
            tool_arguments, tool_name=tool_name, context="Anthropic XML tool invoke"
        )
        if isinstance(parsed_args, dict):
            parameters = "".join(
                f"<{param}>{val}</{param}>\n" for param, val in parsed_args.items()
            )
        else:
            parameters = f"<result>{parsed_args}</result>\n"
        invokes += f"<invoke>\n<tool_name>{tool_name}</tool_name>\n<parameters>\n{parameters}</parameters>\n</invoke>\n"

    anthropic_tool_invoke = f"<function_calls>\n{invokes}</function_calls>"

    return anthropic_tool_invoke

