
def test_raise_on_nuisance_python_single(df, using_infer_string):
    # GH 38815
    grouped = df.groupby("A")

    err = ValueError
    msg = "could not convert"
    if using_infer_string:
        err = TypeError
        msg = "dtype 'str' does not support operation 'skew'"
    with pytest.raises(err, match=msg):
        grouped.skew()

