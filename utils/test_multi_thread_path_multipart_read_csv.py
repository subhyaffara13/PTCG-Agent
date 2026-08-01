
def test_multi_thread_path_multipart_read_csv(tmp_path, all_parsers):
    # see gh-11786
    num_tasks = 4
    num_rows = 48

    parser = all_parsers
    file_name = "__thread_pool_reader__.csv"
    df = DataFrame(
        {
            "a": np.random.default_rng(2).random(num_rows),
            "b": np.random.default_rng(2).random(num_rows),
            "c": np.random.default_rng(2).random(num_rows),
            "d": np.random.default_rng(2).random(num_rows),
            "e": np.random.default_rng(2).random(num_rows),
            "foo": ["foo"] * num_rows,
            "bar": ["bar"] * num_rows,
            "baz": ["baz"] * num_rows,
            "date": pd.date_range("20000101 09:00:00", periods=num_rows, freq="s"),
            "int": np.arange(num_rows, dtype="int64"),
        }
    )

    path = tmp_path / file_name
    df.to_csv(path)

    result = _generate_multi_thread_dataframe(parser, path, num_rows, num_tasks)

    expected = df[:]
    expected["date"] = expected["date"].astype("M8[us]")
    tm.assert_frame_equal(result, expected)

