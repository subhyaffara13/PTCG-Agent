
def paper_2_case(explicit_edge_wt=True, directed=False):
    # problem specific constants
    byte_block_size = 32

    # configuration
    if directed:
        example_2 = nx.DiGraph()
    else:
        example_2 = nx.Graph()

    if explicit_edge_wt:
        edic = {EWL: 1}
        wtu = EWL
    else:
        edic = {}
        wtu = None

    # graph creation
    example_2.add_edge("name", "home_address", **edic)
    example_2.add_edge("name", "education", **edic)
    example_2.add_edge("education", "bs", **edic)
    example_2.add_edge("education", "ms", **edic)
    example_2.add_edge("education", "phd", **edic)
    example_2.add_edge("name", "telephone", **edic)
    example_2.add_edge("telephone", "home", **edic)
    example_2.add_edge("telephone", "office", **edic)
    example_2.add_edge("office", "no1", **edic)
    example_2.add_edge("office", "no2", **edic)

    example_2.nodes["name"][NWL] = 20
    example_2.nodes["education"][NWL] = 10
    example_2.nodes["bs"][NWL] = 1
    example_2.nodes["ms"][NWL] = 1
    example_2.nodes["phd"][NWL] = 1
    example_2.nodes["home_address"][NWL] = 8
    example_2.nodes["telephone"][NWL] = 8
    example_2.nodes["home"][NWL] = 8
    example_2.nodes["office"][NWL] = 4
    example_2.nodes["no1"][NWL] = 1
    example_2.nodes["no2"][NWL] = 1

    # partitioning
    clusters_2 = {
        frozenset(x)
        for x in nx.community.lukes_partitioning(
            example_2, byte_block_size, node_weight=NWL, edge_weight=wtu
        )
    }

    return clusters_2

