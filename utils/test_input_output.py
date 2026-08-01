
def test_input_output():
    l = [nx.Graph([(1, 2)]), nx.Graph([(3, 4)], awesome=True)]
    U = nx.disjoint_union_all(l)
    assert len(l) == 2
    assert U.graph["awesome"]
    C = nx.compose_all(l)
    assert len(l) == 2
    l = [nx.Graph([(1, 2)]), nx.Graph([(1, 2)])]
    R = nx.intersection_all(l)
    assert len(l) == 2

