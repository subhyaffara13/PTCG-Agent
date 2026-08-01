
def test_mathieusprime():
    assert isinstance(mathieusprime(a, q, z), mathieusprime)
    assert mathieusprime(a, 0, z) == sqrt(a)*cos(sqrt(a)*z)
    assert diff(mathieusprime(a, q, z), z) == (-a + 2*q*cos(2*z))*mathieus(a, q, z)

