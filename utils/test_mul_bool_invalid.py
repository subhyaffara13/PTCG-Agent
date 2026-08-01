
def test_mul_bool_invalid(any_string_dtype):
    # GH#62595
    dtype = any_string_dtype
    ser = Series(["a", "b", "c"], dtype=dtype)

    if dtype == object:
        pytest.skip("This is not expect to raise")
    elif dtype.storage == "python":
        msg = "Cannot multiply StringArray by bools. Explicitly cast to integers"
    else:
        msg = "Can only string multiply by an integer"

    with pytest.raises(TypeError, match=msg):
        False * ser
    with pytest.raises(TypeError, match=msg):
        ser * True
    with pytest.raises(TypeError, match=msg):
        ser * np.array([True, False, True], dtype=bool)
    with pytest.raises(TypeError, match=msg):
        np.array([True, False, True], dtype=bool) * ser

