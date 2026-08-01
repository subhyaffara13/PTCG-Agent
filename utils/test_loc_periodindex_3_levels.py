
def test_loc_periodindex_3_levels():
    # GH#24091
    p_index = PeriodIndex(
        ["20181101 1100", "20181101 1200", "20181102 1300", "20181102 1400"],
        name="datetime",
        freq="B",
    )
    mi_series = DataFrame(
        [["A", "B", 1.0], ["A", "C", 2.0], ["Z", "Q", 3.0], ["W", "F", 4.0]],
        index=p_index,
        columns=["ONE", "TWO", "VALUES"],
    )
    mi_series = mi_series.set_index(["ONE", "TWO"], append=True)["VALUES"]
    assert mi_series.loc[(p_index[0], "A", "B")] == 1.0

