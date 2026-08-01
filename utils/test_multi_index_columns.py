
def test_multi_index_columns():
    df = pd.DataFrame(
        {("A", 1): np.array([[0, 1, 2], np.nan, [], (3, 4)], dtype=object), ("A", 2): 1}
    )

    result = df.explode(("A", 1))
    expected = pd.DataFrame(
        {
            ("A", 1): pd.Series(
                [0, 1, 2, np.nan, np.nan, 3, 4],
                index=pd.Index([0, 0, 0, 1, 2, 3, 3]),
                dtype=object,
            ),
            ("A", 2): 1,
        }
    )
    tm.assert_frame_equal(result, expected)

