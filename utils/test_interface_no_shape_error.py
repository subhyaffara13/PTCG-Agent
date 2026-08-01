
def test_interface_no_shape_error():
    class ArrayLike:
        __array_interface__ = {"data": None, "typestr": "f8"}

    with pytest.raises(ValueError, match="Missing __array_interface__ shape"):
        np.array(ArrayLike())

