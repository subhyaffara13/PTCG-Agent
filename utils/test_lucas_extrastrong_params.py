
def test_lucas_extrastrong_params():
    assert _lucas_extrastrong_params(3) == (5, 3, 1)
    assert _lucas_extrastrong_params(5) == (12, 4, 1)
    assert _lucas_extrastrong_params(7) == (5, 3, 1)
    assert _lucas_extrastrong_params(9) == (0, 0, 0)
    assert _lucas_extrastrong_params(11) == (21, 5, 1)
    assert _lucas_extrastrong_params(59) == (32, 6, 1)
    assert _lucas_extrastrong_params(479) == (117, 11, 1)

