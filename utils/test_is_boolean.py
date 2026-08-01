
def test_is_boolean():
    assert isinstance(True, Boolean) is False
    assert isinstance(true, Boolean) is True
    assert 1 == True
    assert 1 != true
    assert (1 == true) is False
    assert 0 == False
    assert 0 != false
    assert (0 == false) is False
    assert true.is_Boolean is True
    assert (A & B).is_Boolean
    assert (A | B).is_Boolean
    assert (~A).is_Boolean
    assert (A ^ B).is_Boolean
    assert A.is_Boolean != isinstance(A, Boolean)
    assert isinstance(A, Boolean)


def test_is_boolean(dtype, expected):
    dtype = NumpyEADtype(dtype)
    assert dtype._is_boolean is expected

