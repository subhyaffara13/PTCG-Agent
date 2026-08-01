
def test_linear_3eq_order1_type4_long_check():
    eq, sol = _linear_3eq_order1_type4_long()
    assert checksysodesol(eq, sol) == (True, [0, 0, 0])

