
def test_sub_period():
    arr = PeriodArray._from_sequence(["2000", "2001"], dtype="period[D]")
    other = pd.Period("2000", freq="M")
    with pytest.raises(IncompatibleFrequency, match="freq"):
        arr - other

