import sys

def min_fill_in_heuristic(graph_dict):
    """Implements the Minimum Degree heuristic.

    graph_dict: dict keyed by node to sets of neighbors (no self-loops)

    Returns the node from the graph, where the number of edges added when
    turning the neighborhood of the chosen node into clique is as small as
    possible. This algorithm chooses the nodes using the Minimum Fill-In
    heuristic. The running time of the algorithm is :math:`O(V^3)` and it uses
    additional constant memory.
    """

    if len(graph_dict) == 0:
        return None

    min_fill_in_node = None

    min_fill_in = sys.maxsize

    # sort nodes by degree
    nodes_by_degree = sorted(graph_dict, key=lambda x: len(graph_dict[x]))
    min_degree = len(graph_dict[nodes_by_degree[0]])

    # abort condition (handle complete graph)
    if min_degree == len(graph_dict) - 1:
        return None

    for node in nodes_by_degree:
        num_fill_in = 0
        nbrs = graph_dict[node]
        for nbr in nbrs:
            # count how many nodes in nbrs current nbr is not connected to
            # subtract 1 for the node itself
            num_fill_in += len(nbrs - graph_dict[nbr]) - 1
            if num_fill_in >= 2 * min_fill_in:
                break

        num_fill_in /= 2  # divide by 2 because of double counting

        if num_fill_in < min_fill_in:  # update min-fill-in node
            if num_fill_in == 0:
                return node
            min_fill_in = num_fill_in
            min_fill_in_node = node

    return min_fill_in_node

