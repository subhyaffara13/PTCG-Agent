
def test_reductions_return_types(
    dropna, data, all_numeric_reductions, using_python_scalars
):
    op = all_numeric_reductions
    s = pd.Series(data)
    if dropna:
        s = s.dropna()

    if using_python_scalars:
        expected = {
            "sum": int,
            "prod": int,
            "count": int,
            "min": bool,
            "max": bool,
        }.get(op, float)
    else:
        expected = {
            "sum": np.int_,
            "prod": np.int_,
            "count": np.integer,
            "min": np.bool_,
            "max": np.bool_,
        }.get(op, np.float64)
    result = getattr(s, op)()
    assert isinstance(result, expected), f"{type(result)} vs {expected}"

