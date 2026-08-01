
def test_index_col_large_csv(temp_file, all_parsers, monkeypatch):
    # https://github.com/pandas-dev/pandas/issues/37094
    parser = all_parsers

    ARR_LEN = 100
    df = DataFrame(
        {
            "a": range(ARR_LEN + 1),
            "b": np.random.default_rng(2).standard_normal(ARR_LEN + 1),
        }
    )

    df.to_csv(temp_file, index=False)
    with monkeypatch.context() as m:
        m.setattr("pandas.core.algorithms._MINIMUM_COMP_ARR_LEN", ARR_LEN)
        result = parser.read_csv(temp_file, index_col=[0])

    tm.assert_frame_equal(result, df.set_index("a"))

