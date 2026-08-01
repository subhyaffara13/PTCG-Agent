
def test_coulomb():
    # Note: most tests are doctests
    # Test for a bug:
    mp.dps = 15
    assert coulombg(mpc(-5,0),2,3).ae(20.087729487721430394)

