
def _neighborhood_aggregate_directed(G, node, node_labels, edge_attr=None):
    """
    Compute new labels for given node in a directed graph by aggregating
    the labels of each node's neighbors.
    """
    successor_labels = []
    for nbr in G.successors(node):
        prefix = "s_" + "" if edge_attr is None else str(G[node][nbr][edge_attr])
        successor_labels.append(prefix + node_labels[nbr])

    predecessor_labels = []
    for nbr in G.predecessors(node):
        prefix = "p_" + "" if edge_attr is None else str(G[nbr][node][edge_attr])
        predecessor_labels.append(prefix + node_labels[nbr])
    return (
        node_labels[node]
        + "".join(sorted(successor_labels))
        + "".join(sorted(predecessor_labels))
    )

