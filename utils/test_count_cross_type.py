
def test_count_cross_type(typ):
    # GH8169
    # Set float64 dtype to avoid upcast when setting nan below
    vals = np.hstack(
        (
            np.random.default_rng(2).integers(0, 5, (10, 2)),
            np.random.default_rng(2).integers(0, 2, (10, 2)),
        )
    ).astype("float64")

    df = DataFrame(vals, columns=["a", "b", "c", "d"])
    df[df == 2] = np.nan
    expected = df.groupby(["c", "d"]).count()

    df["a"] = df["a"].astype(typ)
    df["b"] = df["b"].astype(typ)
    result = df.groupby(["c", "d"]).count()
    tm.assert_frame_equal(result, expected)

