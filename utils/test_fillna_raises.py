
def test_fillna_raises():
    arr = PeriodArray._from_sequence(["2000", "2001", "2002"], dtype="period[D]")
    with pytest.raises(ValueError, match="Length"):
        arr.fillna(arr[:2])

