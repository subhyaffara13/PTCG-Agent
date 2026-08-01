
def test_to_dict_of_dicts_with_edgedata_multigraph():
    """Multi edge data overwritten when edge_data != None"""
    G = nx.MultiGraph()
    G.add_edge(0, 1, key="a")
    G.add_edge(0, 1, key="b")
    # Multi edge data lost when edge_data is not None
    expected = {0: {1: 10}, 1: {0: 10}}
    assert nx.to_dict_of_dicts(G, edge_data=10) == expected

