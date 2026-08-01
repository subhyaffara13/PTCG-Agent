
def test_gamma_rewrite():
    assert gamma(n).rewrite(factorial) == factorial(n - 1)

