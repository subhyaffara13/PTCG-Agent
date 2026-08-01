
def test_type_check(errors):
    # see gh-11776
    df = DataFrame({"a": [1, -3.14, 7], "b": ["4", "5", "6"]})
    kwargs = {"errors": errors} if errors is not None else {}
    with pytest.raises(TypeError, match="1-d array"):
        to_numeric(df, **kwargs)

