
def _should_reregister_graph(
    original_graph: list[_OverrideNode],
    new_graph: list[_OverrideNode],
    *,
    force_reregister: bool = False,
) -> bool:
    """
    Determine if a graph needs reregistration based on changes.

    Args:
        original_graph: The original graph before modification
        new_graph: The graph after modification
        force_reregister: If True, always reregister regardless of changes

    Returns:
        bool: True if reregistration is needed
    """
    if force_reregister:
        return True

    # Check if the graph structure has changed
    return original_graph != new_graph

