
def test_chi2_inv_smalldf():
    assert_allclose(special.chdtri(0.6, 1 - 0.957890536704110), 3,
                    atol=1.5e-7, rtol=0)

