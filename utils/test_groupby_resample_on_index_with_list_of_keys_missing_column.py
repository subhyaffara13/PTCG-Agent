
def test_groupby_resample_on_index_with_list_of_keys_missing_column():
    # GH 50876
    df = DataFrame(
        data={
            "group": [0, 0, 0, 0, 1, 1, 1, 1],
            "val": [3, 1, 4, 1, 5, 9, 2, 6],
        },
        index=Series(
            date_range(start="2016-01-01", periods=8),
            name="date",
        ),
    )
    gb = df.groupby("group")
    rs = gb.resample("2D")
    with pytest.raises(KeyError, match="Columns not found"):
        rs[["val_not_in_dataframe"]]

