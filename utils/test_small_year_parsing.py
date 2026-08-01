
def test_small_year_parsing():
    per1 = Period("0001-01-07", "D")
    assert per1.year == 1
    assert per1.day == 7

