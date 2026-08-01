
def test_difficult_univariate():
    """ Since using solve in place of deltaintegrate we're able to perform
    substantially more complex density computations on single continuous random
    variables """
    x = Normal('x', 0, 1)
    assert density(x**3)
    assert density(exp(x**2))
    assert density(log(x))

