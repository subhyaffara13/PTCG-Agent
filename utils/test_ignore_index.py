
def test_ignore_index():
    # GH 34932
    s = pd.Series([[1, 2], [3, 4]])
    result = s.explode(ignore_index=True)
    expected = pd.Series([1, 2, 3, 4], index=[0, 1, 2, 3], dtype=object)
    tm.assert_series_equal(result, expected)


def test_ignore_index():
    # GH 34932
    df = pd.DataFrame({"id": range(0, 20, 10), "values": [list("ab"), list("cd")]})
    result = df.explode("values", ignore_index=True)
    expected = pd.DataFrame(
        {"id": [0, 0, 10, 10], "values": list("abcd")}, index=range(4)
    )
    tm.assert_frame_equal(result, expected)

