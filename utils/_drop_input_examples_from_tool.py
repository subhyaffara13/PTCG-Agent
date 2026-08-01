
def _drop_input_examples_from_tool(tool: dict) -> dict:
    tool_copy = tool.copy()
    tool_copy.pop("input_examples", None)
    function = tool_copy.get("function")
    if isinstance(function, dict):
        function = function.copy()
        function.pop("input_examples", None)
        tool_copy["function"] = function
    return tool_copy

