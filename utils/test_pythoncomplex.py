
def test_pythoncomplex():
    x = Symbol("x")
    assert 4j*x != 4*x*I
    assert 4j*x == 4.0*x*I
    assert 4.1j*x != 4*x*I

