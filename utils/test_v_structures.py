
def test_v_structures(edgelist, expected):
    G = nx.DiGraph(edgelist)
    v_structs = set(nx.dag.v_structures(G))
    assert v_structs == expected

