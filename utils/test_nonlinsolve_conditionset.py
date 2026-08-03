from typing import Tuple

def test_nonlinsolve_conditionset():
    # when solveset failed to solve all the eq
    # return conditionset
    f = Function('f')
    f1 = f(x) - pi/2
    f2 = f(y) - pi*Rational(3, 2)
    intermediate_system = Eq(2*f(x) - pi, 0) & Eq(2*f(y) - 3*pi, 0)
    syms = Tuple(x, y)
    soln = ConditionSet(
        syms,
        intermediate_system,
        S.Complexes**2)
    assert nonlinsolve([f1, f2], [x, y]) == soln

