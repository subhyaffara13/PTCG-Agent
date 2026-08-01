
def test_pydot_issue_7581(tmp_path):
    """Validate that `nx_pydot.pydot_layout` handles nodes
    with characters like "\n", " ".

    Those characters cause `pydot` to escape and quote them on output,
    which caused #7581.
    """
    G = nx.Graph()
    G.add_edges_from([("A\nbig test", "B"), ("A\nbig test", "C"), ("B", "C")])

    graph_layout = nx.nx_pydot.pydot_layout(G, prog="dot")
    assert isinstance(graph_layout, dict)

    # Convert the graph to pydot and back into a graph. There should be no difference.
    P = nx.nx_pydot.to_pydot(G)
    G2 = nx.Graph(nx.nx_pydot.from_pydot(P))
    assert graphs_equal(G, G2)

