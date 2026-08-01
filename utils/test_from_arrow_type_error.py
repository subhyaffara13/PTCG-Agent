
def test_from_arrow_type_error(data):
    # ensure that __from_arrow__ returns a TypeError when getting a wrong
    # array type

    arr = pa.array(data).cast("string")
    with pytest.raises(TypeError, match=None):
        # we don't test the exact error message, only the fact that it raises
        # a TypeError is relevant
        data.dtype.__from_arrow__(arr)

