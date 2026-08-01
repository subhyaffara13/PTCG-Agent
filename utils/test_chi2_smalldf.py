
def test_chi2_smalldf():
    assert_allclose(special.chdtr(0.6, 3), 0.957890536704110, atol=1.5e-7, rtol=0)

