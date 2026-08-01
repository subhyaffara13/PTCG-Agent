
def rooted_tree_isomorphism(t1, root1, t2, root2):
    """
    Return an isomorphic mapping between rooted trees `t1` and `t2` with roots
    `root1` and `root2`, respectively.

    These trees may be either directed or undirected,
    but if they are directed, all edges should flow from the root.

    It returns the isomorphism, a mapping of the nodes of `t1` onto the nodes
    of `t2`, such that two trees are then identical.

    Note that two trees may have more than one isomorphism, and this
    routine just returns one valid mapping.
    This is a subroutine used to implement `tree_isomorphism`, but will
    be somewhat faster if you already have rooted trees.

    Parameters
    ----------
    t1 :  NetworkX graph
        One of the trees being compared

    root1 : node
        A node of `t1` which is the root of the tree

    t2 : NetworkX graph
        The other tree being compared

    root2 : node
        a node of `t2` which is the root of the tree

    Returns
    -------
    isomorphism : list
        A list of pairs in which the left element is a node in `t1`
        and the right element is a node in `t2`.  The pairs are in
        arbitrary order.  If the nodes in one tree is mapped to the names in
        the other, then trees will be identical. Note that an isomorphism
        will not necessarily be unique.

        If `t1` and `t2` are not isomorphic, then it returns the empty list.

    Raises
    ------
    NetworkXError
        If either `t1` or `t2` is not a tree
    """

    if not nx.is_tree(t1):
        raise nx.NetworkXError("t1 is not a tree")
    if not nx.is_tree(t2):
        raise nx.NetworkXError("t2 is not a tree")

    # get the rooted tree formed by combining them
    # with unique names
    (dT, namemap, newroot1, newroot2) = root_trees(t1, root1, t2, root2)

    # Group nodes by their distance from the root
    L = defaultdict(list)
    for n, dist in nx.shortest_path_length(dT, source=0).items():
        L[dist].append(n)

    # height
    h = max(L)

    # each node has a label, initially set to 0
    label = {v: 0 for v in dT}
    # and also ordered_labels and ordered_children
    # which will store ordered tuples
    ordered_labels = {v: () for v in dT}
    ordered_children = {v: () for v in dT}

    # nothing to do on last level so start on h-1
    # also nothing to do for our fake level 0, so skip that
    for i in range(h - 1, 0, -1):
        # update the ordered_labels and ordered_children
        # for any children
        for v in L[i]:
            # nothing to do if no children
            if dT.out_degree(v) > 0:
                # get all the pairs of labels and nodes of children and sort by labels
                # reverse=True to preserve DFS order, see gh-7945
                s = sorted(((label[u], u) for u in dT.successors(v)), reverse=True)

                # invert to give a list of two tuples
                # the sorted labels, and the corresponding children
                ordered_labels[v], ordered_children[v] = list(zip(*s))

        # now collect and sort the sorted ordered_labels
        # for all nodes in L[i], carrying along the node
        forlabel = sorted((ordered_labels[v], v) for v in L[i])

        # now assign labels to these nodes, according to the sorted order
        # starting from 0, where identical ordered_labels get the same label
        current = 0
        for i, (ol, v) in enumerate(forlabel):
            # advance to next label if not 0, and different from previous
            if (i != 0) and (ol != forlabel[i - 1][0]):
                current += 1
            label[v] = current

    # they are isomorphic if the labels of newroot1 and newroot2 are 0
    isomorphism = []
    if label[newroot1] == 0 and label[newroot2] == 0:
        # now lets get the isomorphism by walking the ordered_children
        stack = [(newroot1, newroot2)]
        while stack:
            curr_v, curr_w = stack.pop()
            isomorphism.append((curr_v, curr_w))
            stack.extend(zip(ordered_children[curr_v], ordered_children[curr_w]))

        # get the mapping back in terms of the old names
        # return in sorted order for neatness
        isomorphism = [(namemap[u], namemap[v]) for (u, v) in isomorphism]

    return isomorphism

