
def paper_1_case(float_edge_wt=False, explicit_node_wt=True, directed=False):
    # problem-specific constants
    limit = 3

    # configuration
    if float_edge_wt:
        shift = 0.001
    else:
        shift = 0

    if directed:
        example_1 = nx.DiGraph()
    else:
        example_1 = nx.Graph()

    # graph creation
    example_1.add_edge(1, 2, **{EWL: 3 + shift})
    example_1.add_edge(1, 4, **{EWL: 2 + shift})
    example_1.add_edge(2, 3, **{EWL: 4 + shift})
    example_1.add_edge(2, 5, **{EWL: 6 + shift})

    # node weights
    if explicit_node_wt:
        nx.set_node_attributes(example_1, 1, NWL)
        wtu = NWL
    else:
        wtu = None

    # partitioning
    clusters_1 = {
        frozenset(x)
        for x in nx.community.lukes_partitioning(
            example_1, limit, node_weight=wtu, edge_weight=EWL
        )
    }

    return clusters_1

