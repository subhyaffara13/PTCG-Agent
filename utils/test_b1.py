
def test_B1():
    assert (FiniteSet(i, j, j, k, k, k) | FiniteSet(l, k, j) |
            FiniteSet(j, m, j)) == FiniteSet(i, j, k, l, m)

