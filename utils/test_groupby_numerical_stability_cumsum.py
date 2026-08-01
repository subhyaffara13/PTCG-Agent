
def test_groupby_numerical_stability_cumsum():
    # GH#38934
    data = [1e16, 1e16, 97, 98, -5e15, -5e15, -5e15, -5e15]
    df = DataFrame({"group": [1, 2] * 4, "a": data, "b": data})
    result = df.groupby("group").cumsum()
    exp_data = (
        [1e16] * 2 + [1e16 + 96, 1e16 + 98] + [5e15 + 97, 5e15 + 98] + [97.0, 98.0]
    )
    expected = DataFrame({"a": exp_data, "b": exp_data})
    tm.assert_frame_equal(result, expected, check_exact=True)

