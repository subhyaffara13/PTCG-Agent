
def test_data_frame_value_counts_dropna_true(nulls_fixture):
    # GH 41334
    df = pd.DataFrame(
        {
            "first_name": ["John", "Anne", "John", "Beth"],
            "middle_name": ["Smith", nulls_fixture, nulls_fixture, "Louise"],
        },
    )
    result = df.value_counts()
    expected = pd.Series(
        data=[1, 1],
        index=pd.MultiIndex.from_arrays(
            [("John", "Beth"), ("Smith", "Louise")], names=["first_name", "middle_name"]
        ),
        name="count",
    )

    tm.assert_series_equal(result, expected)

