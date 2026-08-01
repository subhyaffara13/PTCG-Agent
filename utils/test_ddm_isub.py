
def test_ddm_isub():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    ddm_isub(a, b)
    assert a == [[-4, -4], [-4, -4]]

