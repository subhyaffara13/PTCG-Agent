
def test_input_data_is_not_modified_when_building_graph():
    G = nx.path_graph(4)
    input_data = cytoscape_data(G)
    orig_data = copy.deepcopy(input_data)
    # Ensure input is unmodified by cytoscape_graph (gh-4173)
    cytoscape_graph(input_data)
    assert input_data == orig_data

