
def test_one_node_graph():
    embedding_data = {0: []}
    check_embedding_data(embedding_data)


def test_one_node_graph():
    """Second order centrality: single node"""
    G = nx.Graph()
    G.add_node(0)
    G.add_edge(0, 0)
    assert nx.second_order_centrality(G)[0] == 0

