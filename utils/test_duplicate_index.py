
def test_duplicate_index():
    # GH 28005
    s = pd.Series([[1, 2], [3, 4]], index=[0, 0])
    result = s.explode()
    expected = pd.Series([1, 2, 3, 4], index=[0, 0, 0, 0], dtype=object)
    tm.assert_series_equal(result, expected)


def test_duplicate_index(input_dict, input_index, expected_dict, expected_index):
    # GH 28005
    df = pd.DataFrame(input_dict, index=input_index, dtype=object)
    result = df.explode("col1")
    expected = pd.DataFrame(expected_dict, index=expected_index, dtype=object)
    tm.assert_frame_equal(result, expected)

