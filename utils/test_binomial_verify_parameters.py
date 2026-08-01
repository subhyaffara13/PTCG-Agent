
def test_binomial_verify_parameters():
    raises(ValueError, lambda: Binomial('b', .2, .5))
    raises(ValueError, lambda: Binomial('b', 3, 1.5))

