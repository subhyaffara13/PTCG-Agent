
def test_matmul_dot_not_implemented():
    arr_a = coo_array([[1, 2], [3, 4]])
    with pytest.raises(TypeError, match="argument not supported type"):
        arr_a.dot(None)
    with pytest.raises(TypeError, match="arg not supported type"):
        arr_a.tensordot(None)
    with pytest.raises(TypeError, match="unsupported operand type"):
        arr_a @ None
    with pytest.raises(TypeError, match="unsupported operand type"):
        None @ arr_a

