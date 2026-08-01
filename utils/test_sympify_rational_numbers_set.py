
def test_sympify_rational_numbers_set():
    ans = [Rational(3, 10), Rational(1, 5)]
    assert sympify({'.3', '.2'}, rational=True) == FiniteSet(*ans)

