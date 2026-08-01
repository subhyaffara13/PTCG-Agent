
def test_exptrigsimp_noncommutative():
    a,b = symbols('a b', commutative=False)
    x = Symbol('x', commutative=True)
    assert exp(a + x) == exptrigsimp(exp(a)*exp(x))
    p = exp(a)*exp(b) - exp(b)*exp(a)
    assert p == exptrigsimp(p) != 0

