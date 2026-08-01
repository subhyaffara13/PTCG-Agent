
def test_unitary_XGate():
    x = XGate(1, 2)
    x_dagger = Dagger(x)

    assert (x*x_dagger == 1)

