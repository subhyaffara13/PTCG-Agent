
def test_to_dict_of_dicts_with_edgedata_param(edgelist):
    G = nx.Graph()
    G.add_edges_from(edgelist)
    # Innermost dict value == edge_data when edge_data != None.
    # In the case when G has edge data, it is overwritten
    expected = {0: {1: 10}, 1: {0: 10, 2: 10}, 2: {1: 10}}
    assert nx.to_dict_of_dicts(G, edge_data=10) == expected

