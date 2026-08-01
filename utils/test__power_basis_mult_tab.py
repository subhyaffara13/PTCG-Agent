
def test_PowerBasis_mult_tab():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    M = A.mult_tab()
    exp = {0: {0: [1, 0, 0, 0], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0], 3: [0, 0, 0, 1]},
           1: {1: [0, 0, 1, 0], 2: [0, 0, 0, 1], 3: [-1, -1, -1, -1]},
           2: {2: [-1, -1, -1, -1], 3: [1, 0, 0, 0]},
           3: {3: [0, 1, 0, 0]}}
    # We get the table we expect:
    assert M == exp
    # And all entries are of expected type:
    assert all(is_int(c) for u in M for v in M[u] for c in M[u][v])

