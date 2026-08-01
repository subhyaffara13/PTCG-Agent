
def test_sympy__physics__quantum__trace__Tr():
    from sympy.physics.quantum.trace import Tr
    a, b = symbols('a b', commutative=False)
    assert _test_args(Tr(a + b))

