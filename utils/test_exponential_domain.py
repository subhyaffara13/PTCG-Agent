
def test_exponential_domain():
    K = ZZ[E]
    eK = K.from_sympy(E)
    assert K.from_sympy(exp(3)) == eK ** 3
    assert K.convert(exp(3)) == eK ** 3

