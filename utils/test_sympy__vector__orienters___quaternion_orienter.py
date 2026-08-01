
def test_sympy__vector__orienters__QuaternionOrienter():
    from sympy.vector.orienters import QuaternionOrienter
    a, b, c, d = symbols('a b c d')
    assert _test_args(QuaternionOrienter(a, b, c, d))

