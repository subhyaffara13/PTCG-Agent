
def _fista(G, iterations):
    if G.number_of_edges() == 0:
        return 0.0, set()
    if iterations < 1:
        raise ValueError(
            f"The number of iterations must be an integer >= 1. Provided: {iterations}"
        )
    import numpy as np

    # 1. Node Mapping: Assign a unique index to each node and edge
    node_to_idx = {node: idx for idx, node in enumerate(G)}
    num_nodes = G.number_of_nodes()
    num_undirected_edges = G.number_of_edges()

    # 2. Edge Mapping: Assign a unique index to each bidirectional edge
    bidirectional_edges = [(u, v) for u, v in G.edges] + [(v, u) for u, v in G.edges]
    edge_to_idx = {edge: idx for idx, edge in enumerate(bidirectional_edges)}

    num_edges = len(bidirectional_edges)

    # 3. Reverse Edge Mapping: Map each (bidirectional) edge to its reverse edge index
    reverse_edge_idx = np.empty(num_edges, dtype=np.int32)
    for idx in range(num_undirected_edges):
        reverse_edge_idx[idx] = num_undirected_edges + idx
    for idx in range(num_undirected_edges, 2 * num_undirected_edges):
        reverse_edge_idx[idx] = idx - num_undirected_edges

    # 4. Initialize Variables as NumPy Arrays
    x = np.full(num_edges, 0.5, dtype=np.float32)
    y = x.copy()
    z = np.zeros(num_edges, dtype=np.float32)
    b = np.zeros(num_nodes, dtype=np.float32)  # Induced load vector
    tk = 1.0  # Momentum term

    # 5. Precompute Edge Source Indices
    edge_src_indices = np.array(
        [node_to_idx[u] for u, _ in bidirectional_edges], dtype=np.int32
    )

    # 6. Compute Learning Rate
    max_degree = max(deg for _, deg in G.degree)
    # 0.9 for floating point errs when max_degree is very large
    learning_rate = 0.9 / max_degree

    # 7. Iterative Updates
    for _ in range(iterations):
        # 7a. Update b: sum y over outgoing edges for each node
        b[:] = 0.0  # Reset b to zero
        np.add.at(b, edge_src_indices, y)  # b_u = \sum_{v : (u,v) \in E(G)} y_{uv}

        # 7b. Compute z, z_{uv} = y_{uv} - 2 * learning_rate * b_u
        z = y - 2.0 * learning_rate * b[edge_src_indices]

        # 7c. Update Momentum Term
        tknew = (1.0 + math.sqrt(1 + 4.0 * tk**2)) / 2.0

        # 7d. Update x in a vectorized manner, x_{uv} = (z_{uv} - z_{vu} + 1.0) / 2.0
        new_xuv = (z - z[reverse_edge_idx] + 1.0) / 2.0
        clamped_x = np.clip(new_xuv, 0.0, 1.0)  # Clamp x_{uv} between 0 and 1

        # Update y using the FISTA update formula (similar to gradient descent)
        y = (
            clamped_x
            + ((tk - 1.0) / tknew) * (clamped_x - x)
            + (tk / tknew) * (clamped_x - y)
        )

        # Update x
        x = clamped_x

        # Update tk, the momemntum term
        tk = tknew

    # Rebalance the b values! Otherwise performance is a bit suboptimal.
    b[:] = 0.0
    np.add.at(b, edge_src_indices, x)  # b_u = \sum_{v : (u,v) \in E(G)} x_{uv}

    # Extract the actual (approximate) dense subgraph.
    return _fractional_peeling(G, b, x, node_to_idx, edge_to_idx)

