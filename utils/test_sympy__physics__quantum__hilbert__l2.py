
def test_sympy__physics__quantum__hilbert__L2():
    from sympy.physics.quantum.hilbert import L2
    from sympy.core.numbers import oo
    from sympy.sets.sets import Interval
    assert _test_args(L2(Interval(0, oo)))

