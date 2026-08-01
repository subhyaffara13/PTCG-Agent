
def test_apply_typecast_fail():
    df = DataFrame(
        {
            "d": [1.0, 1.0, 1.0, 2.0, 2.0, 2.0],
            "c": np.tile(["a", "b", "c"], 2),
            "v": np.arange(1.0, 7.0),
        }
    )

    def f(group):
        v = group["v"]
        group["v2"] = (v - v.min()) / (v.max() - v.min())
        return group

    result = df.groupby("d", group_keys=False).apply(f)

    expected = df[["c", "v"]]
    expected["v2"] = np.tile([0.0, 0.5, 1], 2)

    tm.assert_frame_equal(result, expected)

