
def test_sdm_monomial_divides():
    assert sdm_monomial_divides((1, 0, 0), (1, 0, 0)) is True
    assert sdm_monomial_divides((1, 0, 0), (1, 2, 1)) is True
    assert sdm_monomial_divides((5, 1, 1), (5, 2, 1)) is True

    assert sdm_monomial_divides((1, 0, 0), (2, 0, 0)) is False
    assert sdm_monomial_divides((1, 1, 0), (1, 0, 0)) is False
    assert sdm_monomial_divides((5, 1, 2), (5, 0, 1)) is False

