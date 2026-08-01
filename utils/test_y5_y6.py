
def test_Y5_Y6():
# Solve y'' + y = 4 [H(t - 1) - H(t - 2)], y(0) = 1, y'(0) = 0 where H is the
# Heaviside (unit step) function (the RHS describes a pulse of magnitude 4 and
# duration 1).  See David A. Sanchez, Richard C. Allen, Jr. and Walter T.
# Kyner, _Differential Equations: An Introduction_, Addison-Wesley Publishing
# Company, 1983, p. 211.  First, take the Laplace transform of the ODE
# => s^2 Y(s) - s + Y(s) = 4/s [e^(-s) - e^(-2 s)]
# where Y(s) is the Laplace transform of y(t)
    t = symbols('t', real=True)
    s = symbols('s')
    y = Function('y')
    Y = Function('Y')
    F = laplace_correspondence(laplace_transform(diff(y(t), t, 2) + y(t)
                                - 4*(Heaviside(t - 1) - Heaviside(t - 2)),
                                t, s, noconds=True), {y: Y})
    D = (
        -F + s**2*Y(s) - s*y(0) + Y(s) - Subs(Derivative(y(t), t), t, 0) -
        4*exp(-s)/s + 4*exp(-2*s)/s)
    assert D == 0
# Now, solve for Y(s) and then take the inverse Laplace transform
#   => Y(s) = s/(s^2 + 1) + 4 [1/s - s/(s^2 + 1)] [e^(-s) - e^(-2 s)]
#   => y(t) = cos t + 4 {[1 - cos(t - 1)] H(t - 1) - [1 - cos(t - 2)] H(t - 2)}
    Yf = solve(F, Y(s))[0]
    Yf = laplace_initial_conds(Yf, t, {y: [1, 0]})
    assert Yf == (s**2*exp(2*s) + 4*exp(s) - 4)*exp(-2*s)/(s*(s**2 + 1))
    yf = inverse_laplace_transform(Yf, s, t)
    yf = yf.collect(Heaviside(t-1)).collect(Heaviside(t-2))
    assert yf == (
        (4 - 4*cos(t - 1))*Heaviside(t - 1) +
        (4*cos(t - 2) - 4)*Heaviside(t - 2) +
        cos(t)*Heaviside(t))

