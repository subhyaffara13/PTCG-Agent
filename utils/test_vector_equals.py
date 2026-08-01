
def test_vector_equals():
    assert (2*i).equals(j) is False
    assert i.equals(i) is True

    # https://github.com/sympy/sympy/issues/25915
    A = (sqrt(2) + sqrt(6)) / sqrt(sqrt(3) + 2)
    assert (A*i).equals(2*i) is True
    assert (A*i).equals(3*i) is False

    # Test comparing vectors in different coordinate systems
    D = C.orient_new_axis('D', pi/2, C.k)
    assert (D.i).equals(C.j) is True
    assert (D.i).equals(C.i) is False

