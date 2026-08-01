
def test_unstack_multi_index_categorical_values():
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    mi = df.stack().index.rename(["major", "minor"])
    ser = Series(["foo"] * len(mi), index=mi, name="category", dtype="category")

    result = ser.unstack()

    dti = ser.index.levels[0]
    c = pd.Categorical(["foo"] * len(dti))
    expected = DataFrame(
        {"A": c, "B": c, "C": c, "D": c},
        columns=Index(list("ABCD"), name="minor"),
        index=dti.rename("major"),
    )
    tm.assert_frame_equal(result, expected)

