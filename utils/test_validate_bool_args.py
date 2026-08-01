
def test_validate_bool_args(value):
    msg = 'For argument "inplace" expected type bool, received type'
    with pytest.raises(ValueError, match=msg):
        pd.eval("2+2", inplace=value)


def test_validate_bool_args(string_series, func, inplace):
    """Tests for error handling related to data types of method arguments."""
    msg = 'For argument "inplace" expected type bool'
    kwargs = {"inplace": inplace}

    if func == "_set_name":
        kwargs["name"] = "hello"

    with pytest.raises(ValueError, match=msg):
        getattr(string_series, func)(**kwargs)

