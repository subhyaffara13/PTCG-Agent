
def test_hermitian_YGate():
    y = YGate(1, 2)
    y_dagger = Dagger(y)

    assert (y == y_dagger)

