
def test_sympy__physics__quantum__spin__CoupledSpinState():
    from sympy.physics.quantum.spin import CoupledSpinState
    assert _test_args(CoupledSpinState(1, 0, (1, 1)))
    assert _test_args(CoupledSpinState(1, 0, (1, S.Half, S.Half)))
    assert _test_args(CoupledSpinState(
        1, 0, (1, S.Half, S.Half), ((2, 3, S.Half), (1, 2, 1)) ))
    j, m, j1, j2, j3, j12, x = symbols('j m j1:4 j12 x')
    assert CoupledSpinState(
        j, m, (j1, j2, j3)).subs(j2, x) == CoupledSpinState(j, m, (j1, x, j3))
    assert CoupledSpinState(j, m, (j1, j2, j3), ((1, 3, j12), (1, 2, j)) ).subs(j12, x) == \
        CoupledSpinState(j, m, (j1, j2, j3), ((1, 3, x), (1, 2, j)) )

