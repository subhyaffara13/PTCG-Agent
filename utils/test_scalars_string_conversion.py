
def test_scalars_string_conversion(data, dtype):
    try:
        str_vals = [str(d.decode('utf-8')) for d in data]
    except AttributeError:
        str_vals = [str(d) for d in data]
    if dtype.coerce:
        assert_array_equal(
            np.array(data, dtype=dtype),
            np.array(str_vals, dtype=dtype),
        )
    else:
        with pytest.raises(ValueError):
            np.array(data, dtype=dtype)

