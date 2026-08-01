
def _dfbnb(G, k, DF_tree, max_GBC, root, D, max_group, nodes, greedy):
    # stopping condition - if we found a group of size k and with higher GBC then prune
    if len(DF_tree.nodes[root]["GM"]) == k and DF_tree.nodes[root]["GBC"] > max_GBC:
        return DF_tree.nodes[root]["GBC"], DF_tree, DF_tree.nodes[root]["GM"]
    # stopping condition - if the size of group members equal to k or there are less than
    # k - |GM| in the candidate list or the heuristic function plus the GBC is below the
    # maximal GBC found then prune
    if (
        len(DF_tree.nodes[root]["GM"]) == k
        or len(DF_tree.nodes[root]["CL"]) <= k - len(DF_tree.nodes[root]["GM"])
        or DF_tree.nodes[root]["GBC"] + DF_tree.nodes[root]["heu"] <= max_GBC
    ):
        return max_GBC, DF_tree, max_group

    # finding the heuristic of both children
    node_p, node_m, DF_tree = _heuristic(k, root, DF_tree, D, nodes, greedy)

    # finding the child with the bigger heuristic + GBC and expand
    # that node first if greedy then only expand the plus node
    if greedy:
        max_GBC, DF_tree, max_group = _dfbnb(
            G, k, DF_tree, max_GBC, node_p, D, max_group, nodes, greedy
        )

    elif (
        DF_tree.nodes[node_p]["GBC"] + DF_tree.nodes[node_p]["heu"]
        > DF_tree.nodes[node_m]["GBC"] + DF_tree.nodes[node_m]["heu"]
    ):
        max_GBC, DF_tree, max_group = _dfbnb(
            G, k, DF_tree, max_GBC, node_p, D, max_group, nodes, greedy
        )
        max_GBC, DF_tree, max_group = _dfbnb(
            G, k, DF_tree, max_GBC, node_m, D, max_group, nodes, greedy
        )
    else:
        max_GBC, DF_tree, max_group = _dfbnb(
            G, k, DF_tree, max_GBC, node_m, D, max_group, nodes, greedy
        )
        max_GBC, DF_tree, max_group = _dfbnb(
            G, k, DF_tree, max_GBC, node_p, D, max_group, nodes, greedy
        )
    return max_GBC, DF_tree, max_group

