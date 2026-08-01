
def test_multivar_0a():
    assert Order(exp(1/x)*exp(1/y)).expr == exp(1/x)*exp(1/y)

