
def test_hermitian_ZGate():
    z = ZGate(1, 2)
    z_dagger = Dagger(z)

    assert (z == z_dagger)

