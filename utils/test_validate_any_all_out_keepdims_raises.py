
def test_validate_any_all_out_keepdims_raises(kwargs, func):
    ser = Series([1, 2])
    param = next(iter(kwargs))
    name = func.__name__

    msg = (
        f"the '{param}' parameter is not "
        "supported in the pandas "
        rf"implementation of {name}\(\)"
    )
    with pytest.raises(ValueError, match=msg):
        func(ser, **kwargs)

