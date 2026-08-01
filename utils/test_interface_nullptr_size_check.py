
def test_interface_nullptr_size_check():
    # Note that prior to NumPy 2.4 the below took the scalar path (if shape had size 1)
    class ArrayLike:
        __array_interface__ = {"data": (0, True), "typestr": "f8", "shape": ()}

    with pytest.raises(ValueError, match="data is NULL but array contains data"):
        np.array(ArrayLike())

