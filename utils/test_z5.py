
def test_Z5():
    # Second order ODE with initial conditions---solve directly
    # transform: f(t) = sin(2 t)/8 - t cos(2 t)/4
    C1, C2 = symbols('C1 C2')
    # initial conditions not supported, this is a manual workaround
    # https://github.com/sympy/sympy/issues/4720
    eq = Derivative(f(x), x, 2) + 4*f(x) - sin(2*x)
    sol = dsolve(eq, f(x))
    f0 = Lambda(x, sol.rhs)
    assert f0(x) == C2*sin(2*x) + (C1 - x/4)*cos(2*x)
    f1 = Lambda(x, diff(f0(x), x))
    # TODO: Replace solve with solveset, when it works for solveset
    const_dict = solve((f0(0), f1(0)))
    result = f0(x).subs(C1, const_dict[C1]).subs(C2, const_dict[C2])
    assert result == -x*cos(2*x)/4 + sin(2*x)/8
    # Result is OK, but ODE solving with initial conditions should be
    # supported without all this manual work
    raise NotImplementedError('ODE solving with initial conditions \
not supported')

