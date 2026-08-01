
def test_unitary_YGate():
    y = YGate(1, 2)
    y_dagger = Dagger(y)

    assert (y*y_dagger == 1)

