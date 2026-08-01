
def test_repr_small():
    arr = PeriodArray._from_sequence(["2000", "2001"], dtype="period[D]")
    result = str(arr)
    expected = (
        "<PeriodArray>\n['2000-01-01', '2001-01-01']\nLength: 2, dtype: period[D]"
    )
    assert result == expected

