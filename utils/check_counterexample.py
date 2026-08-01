
def check_counterexample(G, sub_graph):
    """Raises an exception if the counterexample is wrong.

    Parameters
    ----------
    G : NetworkX graph
    subdivision_nodes : set
        A set of nodes inducing a subgraph as a counterexample
    """
    # 1. Create the sub graph
    sub_graph = nx.Graph(sub_graph)

    # 2. Remove self loops
    for u in sub_graph:
        if sub_graph.has_edge(u, u):
            sub_graph.remove_edge(u, u)

    # keep track of nodes we might need to contract
    contract = list(sub_graph)

    # 3. Contract Edges
    while len(contract) > 0:
        contract_node = contract.pop()
        if contract_node not in sub_graph:
            # Node was already contracted
            continue
        degree = sub_graph.degree[contract_node]
        # Check if we can remove the node
        if degree == 2:
            # Get the two neighbors
            neighbors = iter(sub_graph[contract_node])
            u = next(neighbors)
            v = next(neighbors)
            # Save nodes for later
            contract.append(u)
            contract.append(v)
            # Contract edge
            sub_graph.remove_node(contract_node)
            sub_graph.add_edge(u, v)

    # 4. Check for isomorphism with K5 or K3_3 graphs
    if len(sub_graph) == 5:
        if not nx.is_isomorphic(nx.complete_graph(5), sub_graph):
            raise nx.NetworkXException("Bad counter example.")
    elif len(sub_graph) == 6:
        if not nx.is_isomorphic(nx.complete_bipartite_graph(3, 3), sub_graph):
            raise nx.NetworkXException("Bad counter example.")
    else:
        raise nx.NetworkXException("Bad counter example.")

