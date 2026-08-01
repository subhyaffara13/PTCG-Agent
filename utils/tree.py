
def tree(node, assumptions=True):
    """
    Returns a tree representation of "node" as a string.

    It uses print_node() together with pprint_nodes() on node.args recursively.

    Parameters
    ==========

    assumptions : bool, optional
        The flag to decide whether to print out all the assumption data
        (such as ``is_integer`, ``is_real``) associated with the
        expression or not.

        Enabling the flag makes the result verbose, and the printed
        result may not be deterministic because of the randomness used
        in backtracing the assumptions.

    See Also
    ========

    print_tree

    """
    subtrees = []
    for arg in node.args:
        subtrees.append(tree(arg, assumptions=assumptions))
    s = print_node(node, assumptions=assumptions) + pprint_nodes(subtrees)
    return s


def tree(request, leaf_size):
    left = request.param
    return IntervalTree(left, left + 2, leaf_size=leaf_size)

