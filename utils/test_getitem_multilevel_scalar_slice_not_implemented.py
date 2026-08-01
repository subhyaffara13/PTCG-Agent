
def test_getitem_multilevel_scalar_slice_not_implemented(
    multiindex_year_month_day_dataframe_random_data,
):
    # not implementing this for now
    df = multiindex_year_month_day_dataframe_random_data
    ser = df["A"]

    msg = r"\(2000, slice\(3, 4, None\)\)"
    with pytest.raises(TypeError, match=msg):
        ser[2000, 3:4]

