
def test_exp_substitution():
    assert integrate(1/sqrt(1-exp(2*x))) == log(sqrt(1 - exp(2*x)) - 1)/2 - log(sqrt(1 - exp(2*x)) + 1)/2

