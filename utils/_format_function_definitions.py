
def _format_function_definitions(tools):
    """Formats tool definitions in the format that OpenAI appears to use.
    Based on https://github.com/forestwanglin/openai-java/blob/main/jtokkit/src/main/java/xyz/felh/openai/jtokkit/utils/TikTokenUtils.java
    """
    lines = []
    lines.append("namespace functions {")
    lines.append("")
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        function = tool.get("function")
        if not isinstance(function, dict):
            # Anthropic tool shape → OpenAI function dict for token counting.
            params = tool.get("input_schema") or tool.get("parameters") or {}
            if not isinstance(params, dict):
                params = {}
            function = {
                "name": tool.get("name"),
                "description": tool.get("description"),
                "parameters": params,
            }
        function_name = function.get("name")
        if not function_name:
            # Skip malformed tools missing a name to avoid emitting
            # ``type None = ...`` which would produce inaccurate token counts.
            continue
        if function_description := function.get("description"):
            lines.append(f"// {function_description}")
        parameters = function.get("parameters") or {}
        if not isinstance(parameters, dict):
            parameters = {}
        properties = parameters.get("properties")
        if properties and properties.keys():
            lines.append(f"type {function_name} = (_: {{")
            lines.append(_format_object_parameters(parameters, 0))
            lines.append("}) => any;")
        else:
            lines.append(f"type {function_name} = () => any;")
        lines.append("")
    lines.append("} // namespace functions")
    return "\n".join(lines)

