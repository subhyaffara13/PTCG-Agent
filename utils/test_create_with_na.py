
def test_create_with_na(dtype):
    if not hasattr(dtype, "na_object"):
        pytest.skip("does not have an na object")
    na_val = dtype.na_object
    string_list = ["hello", na_val, "world"]
    arr = np.array(string_list, dtype=dtype)
    assert str(arr) == "[" + " ".join([repr(s) for s in string_list]) + "]"
    assert arr[1] is dtype.na_object

