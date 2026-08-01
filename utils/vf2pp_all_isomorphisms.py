
def vf2pp_all_isomorphisms(G1, G2, node_label=None, default_label=None):
    """Yields all the possible mappings between G1 and G2.

    Parameters
    ----------
    G1, G2 : NetworkX Graph or MultiGraph instances.
        The two graphs to check for isomorphism.

    node_label : str, optional
        The name of the node attribute to be used when comparing nodes.
        The default is `None`, meaning node attributes are not considered
        in the comparison. Any node that doesn't have the `node_label`
        attribute uses `default_label` instead.

    default_label : scalar
        Default value to use when a node doesn't have an attribute
        named `node_label`. Default is `None`.

    Yields
    ------
    dict
        Isomorphic mapping between the nodes in `G1` and `G2`.
    """
    if G1.number_of_nodes() == 0 or G2.number_of_nodes() == 0:
        return False

    # Create the degree dicts based on graph type
    if G1.is_directed():
        G1_degree = {
            n: (in_degree, out_degree)
            for (n, in_degree), (_, out_degree) in zip(G1.in_degree, G1.out_degree)
        }
        G2_degree = {
            n: (in_degree, out_degree)
            for (n, in_degree), (_, out_degree) in zip(G2.in_degree, G2.out_degree)
        }
    else:
        G1_degree = dict(G1.degree)
        G2_degree = dict(G2.degree)

    if not G1.is_directed():
        find_candidates = _find_candidates
        restore_Tinout = _restore_Tinout
    else:
        find_candidates = _find_candidates_Di
        restore_Tinout = _restore_Tinout_Di

    # Check that both graphs have the same number of nodes and degree sequence
    if G1.order() != G2.order():
        return False
    if sorted(G1_degree.values()) != sorted(G2_degree.values()):
        return False

    # Initialize parameters and cache necessary information about degree and labels
    graph_params, state_params = _initialize_parameters(
        G1, G2, G2_degree, node_label, default_label
    )

    # Check if G1 and G2 have the same labels, and that number of nodes per label
    # is equal between the two graphs
    if not _precheck_label_properties(graph_params):
        return False

    # Calculate the optimal node ordering
    node_order = _matching_order(graph_params)

    # Initialize the stack
    stack = []
    candidates = iter(
        find_candidates(node_order[0], graph_params, state_params, G1_degree)
    )
    stack.append((node_order[0], candidates))

    mapping = state_params.mapping
    reverse_mapping = state_params.reverse_mapping

    # Index of the node from the order, currently being examined
    matching_node = 1

    while stack:
        current_node, candidate_nodes = stack[-1]

        try:
            candidate = next(candidate_nodes)
        except StopIteration:
            # If no remaining candidates, return to a previous state, and follow another branch
            stack.pop()
            matching_node -= 1
            if stack:
                # Pop the previously added u-v pair, and look for a different candidate _v for u
                popped_node1, _ = stack[-1]
                popped_node2 = mapping[popped_node1]
                mapping.pop(popped_node1)
                reverse_mapping.pop(popped_node2)
                restore_Tinout(popped_node1, popped_node2, graph_params, state_params)
            continue

        if _feasibility(current_node, candidate, graph_params, state_params):
            # Terminate if mapping is extended to its full
            if len(mapping) == G2.number_of_nodes() - 1:
                cp_mapping = mapping.copy()
                cp_mapping[current_node] = candidate
                yield cp_mapping
                continue

            # Feasibility rules pass, so extend the mapping and update the parameters
            mapping[current_node] = candidate
            reverse_mapping[candidate] = current_node
            _update_Tinout(current_node, candidate, graph_params, state_params)
            # Append the next node and its candidates to the stack
            candidates = iter(
                find_candidates(
                    node_order[matching_node], graph_params, state_params, G1_degree
                )
            )
            stack.append((node_order[matching_node], candidates))
            matching_node += 1

