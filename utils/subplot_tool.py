
def subplot_tool(targetfig: Figure | None = None) -> SubplotTool | None:
    """
    Launch a subplot tool window for a figure.

    Returns
    -------
    `matplotlib.widgets.SubplotTool`
    """
    if targetfig is None:
        targetfig = gcf()
    tb = targetfig.canvas.manager.toolbar  # type: ignore[union-attr]
    if hasattr(tb, "configure_subplots"):  # toolbar2
        from matplotlib.backend_bases import NavigationToolbar2
        return cast(NavigationToolbar2, tb).configure_subplots()
    elif hasattr(tb, "trigger_tool"):  # toolmanager
        from matplotlib.backend_bases import ToolContainerBase
        cast(ToolContainerBase, tb).trigger_tool("subplots")
        return None
    else:
        raise ValueError("subplot_tool can only be launched for figures with "
                         "an associated toolbar")

