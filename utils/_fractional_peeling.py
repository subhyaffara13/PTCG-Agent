
def _fractional_peeling(G, b, x, node_to_idx, edge_to_idx):
    """
    Optimized fractional peeling using NumPy arrays.

    Parameters
    ----------
    G : networkx.Graph
        The input graph.
    b : numpy.ndarray
        Induced load vector.
    x : numpy.ndarray
        Fractional edge values.
    node_to_idx : dict
        Mapping from node to index.
    edge_to_idx : dict
        Mapping from edge to index.

    Returns
    -------
    best_density : float
        The best density found.
    best_subgraph : set
        The subset of nodes defining the densest subgraph.
    """
    heap = nx.utils.BinaryHeap()

    remaining_nodes = set(G.nodes)

    # Initialize heap with b values
    for idx, node in enumerate(G):
        heap.insert(node, b[idx])

    num_edges = G.number_of_edges()

    best_density = 0.0
    best_subgraph = set()

    while remaining_nodes:
        num_nodes = len(remaining_nodes)
        current_density = num_edges / num_nodes

        if current_density > best_density:
            best_density = current_density
            best_subgraph = set(remaining_nodes)

        # Pop the node with the smallest b
        node, _ = heap.pop()
        while node not in remaining_nodes:
            node, _ = heap.pop()  # Clean the heap from stale values

        # Update neighbors b values by subtracting fractional x value
        for neighbor in G.neighbors(node):
            if neighbor in remaining_nodes:
                neighbor_idx = node_to_idx[neighbor]
                # Take off fractional value
                b[neighbor_idx] -= x[edge_to_idx[(neighbor, node)]]
                num_edges -= 1
                heap.insert(neighbor, b[neighbor_idx])

        remaining_nodes.remove(node)  # peel off node

    return best_density, best_subgraph

