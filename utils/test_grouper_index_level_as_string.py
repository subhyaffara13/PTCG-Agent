
def test_grouper_index_level_as_string(levels, key_strs, groupers):
    frame = pd.DataFrame(
        {
            "outer": ["a", "a", "a", "b", "b", "b"],
            "inner": [1, 2, 3, 1, 2, 3],
            "A": np.arange(6),
            "B": ["one", "one", "two", "two", "one", "one"],
        }
    )
    frame = frame.set_index(levels)
    if "B" not in key_strs or "outer" in frame.columns:
        result = frame.groupby(key_strs).mean(numeric_only=True)
        expected = frame.groupby(groupers).mean(numeric_only=True)
    else:
        result = frame.groupby(key_strs).mean()
        expected = frame.groupby(groupers).mean()
    tm.assert_frame_equal(result, expected)

