
def test_B4():
    assert (FiniteSet(*(FiniteSet(i, j)*FiniteSet(k, l))) ==
            FiniteSet((i, k), (i, l), (j, k), (j, l)))

