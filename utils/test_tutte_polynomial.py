
def test_tutte_polynomial(G, expected):
    assert nx.tutte_polynomial(G).equals(expected)

