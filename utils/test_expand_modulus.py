
def test_expand_modulus():
    assert ((x + y)**11).expand(modulus=11) == x**11 + y**11
    assert ((x + sqrt(2)*y)**11).expand(modulus=11) == x**11 + 10*sqrt(2)*y**11
    assert (x + y/2).expand(modulus=1) == y/2

    raises(ValueError, lambda: ((x + y)**11).expand(modulus=0))
    raises(ValueError, lambda: ((x + y)**11).expand(modulus=x))

