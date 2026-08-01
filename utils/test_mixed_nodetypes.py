
def test_mixed_nodetypes():
    # Smoke test to make sure no TypeError is raised for mixed node types.
    G = nx.Graph()
    edgelist = [(0, 3, [("weight", 5)]), (0, "1", [("weight", 5)])]
    G.add_edges_from(edgelist)
    G = G.to_directed()
    x = branchings.minimum_spanning_arborescence(G)

