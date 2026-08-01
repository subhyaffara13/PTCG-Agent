
def test_colliders(edgelist, expected):
    G = nx.DiGraph(edgelist)
    colliders = set(nx.dag.colliders(G))
    assert colliders == expected

