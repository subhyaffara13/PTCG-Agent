
def test_chi2c_smalldf():
    assert_allclose(special.chdtrc(0.6, 3), 1 - 0.957890536704110,
                    atol=1.5e-7, rtol=0)

