
def test_fock_space():
    f1 = FockSpace()
    f2 = FockSpace()
    assert isinstance(f1, FockSpace)
    assert f1.dimension is oo
    assert f1 == f2

