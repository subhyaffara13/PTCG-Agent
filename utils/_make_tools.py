
def _make_tools(tools: Iterable[ParseableToolParam] | Omit) -> List[ToolParam] | Omit:
    if not is_given(tools):
        return omit

    converted_tools: List[ToolParam] = []
    for tool in tools:
        if tool["type"] != "function":
            converted_tools.append(tool)
            continue

        if "function" not in tool:
            # standard Responses API case
            converted_tools.append(tool)
            continue

        function = cast(Any, tool)["function"]  # pyright: ignore[reportUnnecessaryCast]
        if not isinstance(function, PydanticFunctionTool):
            raise Exception(
                "Expected Chat Completions function tool shape to be created using `openai.pydantic_function_tool()`"
            )

        assert "parameters" in function
        new_tool = ResponsesPydanticFunctionTool(
            {
                "type": "function",
                "name": function["name"],
                "description": function.get("description"),
                "parameters": function["parameters"],
                "strict": function.get("strict") or False,
            },
            function.model,
        )

        converted_tools.append(new_tool.cast())

    return converted_tools

