
def test_expectation():
    m = Normal('A', [x, y], [[1, 0], [0, 1]])
    assert simplify(E(m[1])) == y

