
def test_arrow_dtype_itemsize_variable_width(type_name):
    # GH 57948

    arrow_type = getattr(pa, type_name)()
    dtype = ArrowDtype(arrow_type)

    assert dtype.itemsize == dtype.numpy_dtype.itemsize

