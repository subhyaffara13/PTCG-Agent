
def test_dot_with_inconsistent_shapes():
    arr_a = coo_array([[[1, 2]], [[3, 4]]])
    arr_b = coo_array([4, 5, 6])
    with pytest.raises(ValueError, match="not aligned for n-D dot"):
        arr_a.dot(arr_b)

