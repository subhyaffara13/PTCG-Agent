
def test_ddm_iadd():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    ddm_iadd(a, b)
    assert a == [[6, 8], [10, 12]]

