
def test_groupby_list_infer_array_like(df):
    result = df.groupby(list(df["A"])).mean(numeric_only=True)
    expected = df.groupby(df["A"]).mean(numeric_only=True)
    tm.assert_frame_equal(result, expected, check_names=False)

    with pytest.raises(KeyError, match=r"^'foo'$"):
        df.groupby(list(df["A"][:-1]))

    # pathological case of ambiguity
    df = DataFrame(
        {
            "foo": [0, 1],
            "bar": [3, 4],
            "val": np.random.default_rng(2).standard_normal(2),
        }
    )

    result = df.groupby(["foo", "bar"]).mean()
    expected = df.groupby([df["foo"], df["bar"]]).mean()[["val"]]

