
def test_add_1():
    assert Order(x + x) == Order(x)
    assert Order(3*x - 2*x**2) == Order(x)
    assert Order(1 + x) == Order(1, x)
    assert Order(1 + 1/x) == Order(1/x)
    # TODO : A better output for Order(log(x) + 1/log(x))
    # could be Order(log(x)). Currently Order for expressions
    # where all arguments would involve a log term would fall
    # in this category and outputs for these should be improved.
    assert Order(log(x) + 1/log(x)) == Order((log(x)**2 + 1)/log(x))
    assert Order(exp(1/x) + x) == Order(exp(1/x))
    assert Order(exp(1/x) + 1/x**20) == Order(exp(1/x))

