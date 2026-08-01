
def test_transform_aligns(func, frame_or_series, expected_values, keys, keys_in_index):
    # GH#45648 - transform should align with the input's index
    df = DataFrame({"a1": [1, 1, 3, 2, 2], "b": [5, 4, 3, 2, 1]})
    if "a2" in keys:
        df["a2"] = df["a1"]
    if keys_in_index:
        df = df.set_index(keys, append=True)

    gb = df.groupby(keys)
    if frame_or_series is Series:
        gb = gb["b"]

    result = gb.transform(func)
    expected = DataFrame({"b": expected_values}, index=df.index)
    if frame_or_series is Series:
        expected = expected["b"]
    tm.assert_equal(result, expected)

