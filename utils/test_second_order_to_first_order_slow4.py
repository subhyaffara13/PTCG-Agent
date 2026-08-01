
def test_second_order_to_first_order_slow4():
    f, g = symbols("f g", cls=Function)
    x, t, x_, t_, d, a, m = symbols("x t x_ t_ d a m")

    eqs4 = [Eq(Derivative(f(t), (t, 2)), t*sin(t)*Derivative(g(t), t) - g(t)*sin(t)),
            Eq(Derivative(g(t), (t, 2)), t*sin(t)*Derivative(f(t), t) - f(t)*sin(t))]
    sol4 = [Eq(f(t), C1*t + t*Integral(C2*exp(-t_)*exp(exp(t_)*cos(exp(t_)))*exp(-sin(exp(t_)))/2 +
                C2*exp(-t_)*exp(-exp(t_)*cos(exp(t_)))*exp(sin(exp(t_)))/2 - C3*exp(-t_)*exp(exp(t_)*cos(exp(t_)))*
                exp(-sin(exp(t_)))/2 +
                C3*exp(-t_)*exp(-exp(t_)*cos(exp(t_)))*exp(sin(exp(t_)))/2, (t_, log(t)))),
            Eq(g(t), C4*t + t*Integral(-C2*exp(-t_)*exp(exp(t_)*cos(exp(t_)))*exp(-sin(exp(t_)))/2 +
                C2*exp(-t_)*exp(-exp(t_)*cos(exp(t_)))*exp(sin(exp(t_)))/2 + C3*exp(-t_)*exp(exp(t_)*cos(exp(t_)))*
                exp(-sin(exp(t_)))/2 + C3*exp(-t_)*exp(-exp(t_)*cos(exp(t_)))*exp(sin(exp(t_)))/2, (t_, log(t))))]
    # XXX: dsolve hangs for this in integration
    assert dsolve_system(eqs4, simplify=False, doit=False) == [sol4]
    assert checksysodesol(eqs4, sol4) == (True, [0, 0])

