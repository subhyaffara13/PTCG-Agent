
def _subtree_sizes(G, root):
    """Return a `dict` of the size of each subtree, for every subtree
    of a tree rooted at a given node.

    For every node in the given tree, consider the new tree that would
    be created by detaching it from its parent node (if any). The
    number of nodes in the resulting tree rooted at that node is then
    assigned as the value for that node in the return dictionary.

    Parameters
    ----------
    G : NetworkX graph
       A tree.

    root : node
       A node in `G`.

    Returns
    -------
    s : dict
       Dictionary of number of nodes in every subtree of this tree,
       keyed on the root node for each subtree.

    Examples
    --------
    >>> _subtree_sizes(nx.path_graph(4), 0)
    {0: 4, 1: 3, 2: 2, 3: 1}

    >>> _subtree_sizes(nx.path_graph(4), 2)
    {2: 4, 1: 2, 0: 1, 3: 1}

    """
    sizes = {root: 1}
    stack = [root]
    for parent, child in nx.dfs_edges(G, root):
        while stack[-1] != parent:
            descendant = stack.pop()
            sizes[stack[-1]] += sizes[descendant]
        stack.append(child)
        sizes[child] = 1
    for child, parent in nx.utils.pairwise(reversed(stack)):
        sizes[parent] += sizes[child]
    return sizes

