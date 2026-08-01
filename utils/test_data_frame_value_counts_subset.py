
def test_data_frame_value_counts_subset(nulls_fixture, columns):
    # GH 50829
    df = pd.DataFrame(
        {
            columns[0]: ["John", "Anne", "John", "Beth"],
            columns[1]: ["Smith", nulls_fixture, nulls_fixture, "Louise"],
        },
    )
    result = df.value_counts(columns[0])
    expected = pd.Series(
        data=[2, 1, 1],
        index=pd.Index(["John", "Anne", "Beth"], name=columns[0]),
        name="count",
    )

    tm.assert_series_equal(result, expected)

