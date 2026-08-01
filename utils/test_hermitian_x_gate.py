
def test_hermitian_XGate():
    x = XGate(1, 2)
    x_dagger = Dagger(x)

    assert (x == x_dagger)

