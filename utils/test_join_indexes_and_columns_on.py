
def test_join_indexes_and_columns_on(df1, df2, left_index, join_type):
    # Construct left_df
    left_df = df1.set_index(left_index)

    # Construct right_df
    right_df = df2.set_index(["outer", "inner"])

    # Result
    expected = (
        left_df.reset_index()
        .join(
            right_df, on=["outer", "inner"], how=join_type, lsuffix="_x", rsuffix="_y"
        )
        .set_index(left_index)
    )

    # Perform join
    result = left_df.join(
        right_df, on=["outer", "inner"], how=join_type, lsuffix="_x", rsuffix="_y"
    )

    tm.assert_frame_equal(result, expected, check_like=True)

