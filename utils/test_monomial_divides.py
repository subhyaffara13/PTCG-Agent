
def test_monomial_divides():
    assert monomial_divides((1, 2, 3), (4, 5, 6)) is True
    assert monomial_divides((1, 2, 3), (0, 5, 6)) is False

