
def test_join_period_index():
    frame_with_period_index = DataFrame(
        data=np.arange(20).reshape(4, 5),
        columns=list("abcde"),
        index=period_range(start="2000", freq="Y", periods=4),
    )
    other = frame_with_period_index.rename(columns=lambda key: f"{key}{key}")

    joined_values = np.concatenate([frame_with_period_index.values] * 2, axis=1)

    joined_cols = frame_with_period_index.columns.append(other.columns)

    joined = frame_with_period_index.join(other)
    expected = DataFrame(
        data=joined_values, columns=joined_cols, index=frame_with_period_index.index
    )

    tm.assert_frame_equal(joined, expected)

