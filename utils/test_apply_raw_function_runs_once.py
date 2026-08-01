
def test_apply_raw_function_runs_once(engine):
    # https://github.com/pandas-dev/pandas/issues/34506
    if engine == "numba":
        pytest.skip("appending to list outside of numba func is not supported")

    df = DataFrame({"a": [1, 2, 3]})
    values = []  # Save row values function is applied to

    def reducing_function(row):
        values.extend(row)

    def non_reducing_function(row):
        values.extend(row)
        return row

    for func in [reducing_function, non_reducing_function]:
        del values[:]

        df.apply(func, engine=engine, raw=True, axis=1)
        assert values == list(df.a.to_list())

