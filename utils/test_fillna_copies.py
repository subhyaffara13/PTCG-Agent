
def test_fillna_copies():
    arr = PeriodArray._from_sequence(["2000", "2001", "2002"], dtype="period[D]")
    result = arr.fillna(pd.Period("2000", "D"))
    assert result is not arr

