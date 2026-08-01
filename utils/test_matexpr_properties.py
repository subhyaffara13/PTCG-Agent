
def test_matexpr_properties():
    assert A.shape == (n, m)
    assert (A * B).shape == (n, l)
    assert A[0, 1].indices == (0, 1)
    assert A[0, 0].symbol == A
    assert A[0, 0].symbol.name == 'A'

