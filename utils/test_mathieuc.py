
def test_mathieuc():
    assert isinstance(mathieuc(a, q, z), mathieuc)
    assert mathieuc(a, 0, z) == cos(sqrt(a)*z)
    assert diff(mathieuc(a, q, z), z) == mathieucprime(a, q, z)

