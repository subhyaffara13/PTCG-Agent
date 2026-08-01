
def test_sympy__physics__quantum__state__Wavefunction():
    from sympy.physics.quantum.state import Wavefunction
    from sympy.functions import sin
    from sympy.functions.elementary.piecewise import Piecewise
    n = 1
    L = 1
    g = Piecewise((0, x < 0), (0, x > L), (sqrt(2//L)*sin(n*pi*x/L), True))
    assert _test_args(Wavefunction(g, x))

