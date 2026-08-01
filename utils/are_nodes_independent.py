
def are_nodes_independent(nodes: list[Node]):
    """
    Check if all of the given nodes are pairwise-data independent.

    Arguments:
        nodes: The nodes to check for data dependencies.

    Returns:
        True if any pair in nodes has a data dependency.
    """
    # For each pair in nodes:
    for i, j in itertools.combinations(nodes, 2):
        if may_depend_on(i, j) or may_depend_on(j, i):
            return False

    return True

