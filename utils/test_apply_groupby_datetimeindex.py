
def test_apply_groupby_datetimeindex():
    # GH 26182
    # groupby apply failed on dataframe with DatetimeIndex

    data = [["A", 10], ["B", 20], ["B", 30], ["C", 40], ["C", 50]]
    df = DataFrame(
        data, columns=["Name", "Value"], index=pd.date_range("2020-09-01", "2020-09-05")
    )

    result = df.groupby("Name").sum()

    expected = DataFrame({"Name": ["A", "B", "C"], "Value": [10, 50, 90]})
    expected.set_index("Name", inplace=True)

    tm.assert_frame_equal(result, expected)

