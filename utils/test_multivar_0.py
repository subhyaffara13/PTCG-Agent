
def test_multivar_0():
    assert Order(x*y).expr == x*y
    assert Order(x*y**2).expr == x*y**2
    assert Order(x*y, x).expr == x
    assert Order(x*y**2, y).expr == y**2
    assert Order(x*y*z).expr == x*y*z
    assert Order(x/y).expr == x/y
    assert Order(x*exp(1/y)).expr == x*exp(1/y)
    assert Order(exp(x)*exp(1/y)).expr == exp(x)*exp(1/y)

