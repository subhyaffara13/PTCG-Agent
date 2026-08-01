
def test_Z6():
    # Second order ODE with initial conditions---solve  using Laplace
    # transform: f(t) = sin(2 t)/8 - t cos(2 t)/4
    t = symbols('t', positive=True)
    s = symbols('s')
    eq = Derivative(f(t), t, 2) + 4*f(t) - sin(2*t)
    F, _, _ = laplace_transform(eq, t, s)
    # Laplace transform for diff() not calculated
    # https://github.com/sympy/sympy/issues/7176
    assert (F == s**2*LaplaceTransform(f(t), t, s) +
            4*LaplaceTransform(f(t), t, s) - 2/(s**2 + 4))

