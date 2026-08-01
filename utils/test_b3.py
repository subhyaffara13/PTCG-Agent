
def test_B3():
    assert (FiniteSet(i, j, k, l, m) - FiniteSet(j) ==
            FiniteSet(i, k, l, m))

