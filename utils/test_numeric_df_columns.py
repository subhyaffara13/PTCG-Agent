
def test_numeric_df_columns(columns):
    # see gh-14827
    df = DataFrame(
        {
            "a": [1.2, decimal.Decimal("3.14"), decimal.Decimal("infinity"), "0.1"],
            "b": [1.0, 2.0, 3.0, 4.0],
        }
    )

    expected = DataFrame({"a": [1.2, 3.14, np.inf, 0.1], "b": [1.0, 2.0, 3.0, 4.0]})
    df[columns] = df[columns].apply(to_numeric)

    tm.assert_frame_equal(df, expected)

