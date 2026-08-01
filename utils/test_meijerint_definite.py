
def test_meijerint_definite():
    v, b = meijerint_definite(x, x, 0, 0)
    assert v.is_zero and b is True
    v, b = meijerint_definite(x, x, oo, oo)
    assert v.is_zero and b is True

