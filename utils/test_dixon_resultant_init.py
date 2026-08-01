
def test_dixon_resultant_init():
    """Test init method of DixonResultant."""
    a = IndexedBase("alpha")

    assert dixon.polynomials == [p, q]
    assert dixon.variables == [x, y]
    assert dixon.n == 2
    assert dixon.m == 2
    assert dixon.dummy_variables == [a[0], a[1]]

