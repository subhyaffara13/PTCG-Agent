
def test_K3():
    a, b = symbols('a, b', real=True)
    assert simplify(abs(1/(a + I/a + I*b))) == 1/sqrt(a**2 + (I/a + b)**2)


def test_K3():
    """Second order centrality: complete graph, as defined in paper"""
    G = nx.complete_graph(3)
    b_answer = {0: 1.414, 1: 1.414, 2: 1.414}

    b = nx.second_order_centrality(G)

    for n in sorted(G):
        assert b[n] == pytest.approx(b_answer[n], abs=1e-2)

