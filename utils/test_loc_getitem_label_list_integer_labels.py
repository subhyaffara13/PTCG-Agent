
def test_loc_getitem_label_list_integer_labels(columns, column_key, expected_columns):
    # gh-14836
    df = DataFrame(
        np.random.default_rng(2).random((3, 3)), columns=columns, index=list("ABC")
    )
    expected = df.iloc[:, expected_columns]
    result = df.loc[["A", "B", "C"], column_key]

    tm.assert_frame_equal(result, expected, check_column_type=True)

