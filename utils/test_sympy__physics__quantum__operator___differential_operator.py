
def test_sympy__physics__quantum__operator__DifferentialOperator():
    from sympy.physics.quantum.operator import DifferentialOperator
    from sympy.core.function import (Derivative, Function)
    f = Function('f')
    assert _test_args(DifferentialOperator(1/x*Derivative(f(x), x), f(x)))

