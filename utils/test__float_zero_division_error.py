
def test_Float_zero_division_error():
    # issue 27165
    assert Float('1.7567e-1417').round(15) == Float(0)

