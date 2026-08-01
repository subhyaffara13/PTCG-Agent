
def test_Float_from_tuple():
    a = Float((0, '1L', 0, 1))
    b = Float((0, '1', 0, 1))
    assert a == b

