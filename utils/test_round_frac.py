
def test_round_frac(val, precision, expected):
    # see gh-1979
    result = tmod._round_frac(val, precision=precision)
    assert result == expected

