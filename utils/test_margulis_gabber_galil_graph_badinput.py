
def test_margulis_gabber_galil_graph_badinput(graph_type):
    with pytest.raises(
        nx.NetworkXError, match="`create_using` must be an undirected multigraph"
    ):
        nx.margulis_gabber_galil_graph(3, create_using=graph_type)

