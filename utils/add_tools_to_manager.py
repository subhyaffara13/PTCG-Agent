
def add_tools_to_manager(toolmanager, tools=None):
    """
    Add multiple tools to a `.ToolManager`.

    Parameters
    ----------
    toolmanager : `.backend_managers.ToolManager`
        Manager to which the tools are added.
    tools : {str: class_like}, optional
        The tools to add in a {name: tool} dict, see
        `.backend_managers.ToolManager.add_tool` for more info. If not specified, then
        defaults to `.default_tools`.
    """
    if tools is None:
        tools = default_tools
    for name, tool in tools.items():
        toolmanager.add_tool(name, tool)

