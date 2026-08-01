
def compare_graphs(left: Graph, right: Graph) -> bool:
    """
    Return True if two graphs are identical, i.e they
        - have the same number of outputs in the same order
        - have the same number of inputs in the same order
        - have the same set of nodes, and identical connectivity
    """

    matcher = SubgraphMatcher(left, match_output=True, match_placeholder=True)
    matches = matcher.match(right)

    return len(matches) > 0

