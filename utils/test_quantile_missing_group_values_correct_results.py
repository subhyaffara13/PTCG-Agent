
def test_quantile_missing_group_values_correct_results(
    key, val, expected_key, expected_val
):
    # GH 28662, GH 33200, GH 33569
    df = DataFrame({"key": key, "val": val})

    expected = DataFrame(
        expected_val, index=Index(expected_key, name="key"), columns=["val"]
    )

    grp = df.groupby("key")

    result = grp.quantile(0.5)
    tm.assert_frame_equal(result, expected)

    result = grp.quantile()
    tm.assert_frame_equal(result, expected)

