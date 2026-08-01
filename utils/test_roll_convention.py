
def test_roll_convention(n, expected, compare):
    assert liboffsets.roll_convention(29, n, compare) == expected[compare]

