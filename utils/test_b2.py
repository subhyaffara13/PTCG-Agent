
def test_B2():
    assert (FiniteSet(i, j, j, k, k, k) & FiniteSet(l, k, j) &
            FiniteSet(j, m, j)) == Intersection({j, m}, {i, j, k}, {j, k, l})

