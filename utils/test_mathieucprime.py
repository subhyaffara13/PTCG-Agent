
def test_mathieucprime():
    assert isinstance(mathieucprime(a, q, z), mathieucprime)
    assert mathieucprime(a, 0, z) == -sqrt(a)*sin(sqrt(a)*z)
    assert diff(mathieucprime(a, q, z), z) == (-a + 2*q*cos(2*z))*mathieuc(a, q, z)

