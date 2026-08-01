
def test_expand_inverse():
    assert (1/(1 + I)).expand(complex=True) == (1 - I)/2
    assert ((1 + 2*I)**(-2)).expand(complex=True) == (-3 - 4*I)/25
    assert ((1 + I)**(-8)).expand(complex=True) == Rational(1, 16)

