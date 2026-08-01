
def test_Identity_index():
    I = Identity(3)
    assert I[0, 0] == I[1, 1] == I[2, 2] == 1
    assert I[1, 0] == I[0, 1] == I[2, 1] == 0
    assert I[i, 0].delta_range == (0, 2)
    raises(IndexError, lambda: I[3, 3])

