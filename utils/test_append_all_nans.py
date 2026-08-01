
def test_append_all_nans(temp_hdfstore, using_infer_string):
    df = DataFrame(
        {
            "A1": np.random.default_rng(2).standard_normal(20),
            "A2": np.random.default_rng(2).standard_normal(20),
        },
        index=np.arange(20),
    )
    df.loc[0:15, :] = np.nan

    # nan some entire rows (dropna=True)
    temp_hdfstore.append("df", df[:10], dropna=True)
    temp_hdfstore.append("df", df[10:], dropna=True)
    tm.assert_frame_equal(temp_hdfstore["df"], df[-4:], check_index_type=True)

    # nan some entire rows (dropna=False)
    temp_hdfstore.append("df2", df[:10], dropna=False)
    temp_hdfstore.append("df2", df[10:], dropna=False)
    tm.assert_frame_equal(temp_hdfstore["df2"], df, check_index_type=True)

    # tests the option io.hdf.dropna_table
    with pd.option_context("io.hdf.dropna_table", False):
        temp_hdfstore.append("df3", df[:10])
        temp_hdfstore.append("df3", df[10:])
        tm.assert_frame_equal(temp_hdfstore["df3"], df)

    with pd.option_context("io.hdf.dropna_table", True):
        temp_hdfstore.append("df4", df[:10])
        temp_hdfstore.append("df4", df[10:])
        tm.assert_frame_equal(temp_hdfstore["df4"], df[-4:])

        # nan some entire rows (string are still written!)
        df = DataFrame(
            {
                "A1": np.random.default_rng(2).standard_normal(20),
                "A2": np.random.default_rng(2).standard_normal(20),
                "B": "foo",
                "C": "bar",
            },
            index=np.arange(20),
        )

        df.loc[0:15, :] = np.nan

        temp_hdfstore.remove("df")
        temp_hdfstore.append("df", df[:10], dropna=True)
        temp_hdfstore.append("df", df[10:], dropna=True)
        result = temp_hdfstore["df"]
        expected = df
        if using_infer_string:
            # TODO: Test is incorrect when not using_infer_string.
            #       Should take the last 4 rows uncondiationally.
            expected = expected[-4:]
        tm.assert_frame_equal(result, expected, check_index_type=True)

        temp_hdfstore.remove("df2")
        temp_hdfstore.append("df2", df[:10], dropna=False)
        temp_hdfstore.append("df2", df[10:], dropna=False)
        tm.assert_frame_equal(temp_hdfstore["df2"], df, check_index_type=True)

        # nan some entire rows (but since we have dates they are still
        # written!)
        df = DataFrame(
            {
                "A1": np.random.default_rng(2).standard_normal(20),
                "A2": np.random.default_rng(2).standard_normal(20),
                "B": "foo",
                "C": "bar",
                "D": Timestamp("2001-01-01").as_unit("ns"),
                "E": Timestamp("2001-01-02").as_unit("ns"),
            },
            index=np.arange(20),
        )

        df.loc[0:15, :] = np.nan

        temp_hdfstore.remove("df")
        temp_hdfstore.append("df", df[:10], dropna=True)
        temp_hdfstore.append("df", df[10:], dropna=True)
        tm.assert_frame_equal(temp_hdfstore["df"], df, check_index_type=True)

        temp_hdfstore.remove("df2")
        temp_hdfstore.append("df2", df[:10], dropna=False)
        temp_hdfstore.append("df2", df[10:], dropna=False)
        tm.assert_frame_equal(temp_hdfstore["df2"], df, check_index_type=True)

