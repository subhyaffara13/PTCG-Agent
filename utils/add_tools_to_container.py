
def add_tools_to_container(container, tools=None):
    """
    Add multiple tools to the container.

    Parameters
    ----------
    container : Container
        `.backend_bases.ToolContainerBase` object that will get the tools
        added.
    tools : list, optional
        List in the form ``[[group1, [tool1, tool2 ...]], [group2, [...]]]``
        where the tools ``[tool1, tool2, ...]`` will display in group1.
        See `.backend_bases.ToolContainerBase.add_tool` for details. If not specified,
        then defaults to `.default_toolbar_tools`.
    """
    if tools is None:
        tools = default_toolbar_tools
    for group, grouptools in tools:
        for position, tool in enumerate(grouptools):
            container.add_tool(tool, group, position)

