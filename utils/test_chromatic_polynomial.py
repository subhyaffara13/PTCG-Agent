
def test_chromatic_polynomial(G, expected):
    assert nx.chromatic_polynomial(G).equals(expected)

