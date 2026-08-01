
def test_second_order_to_first_order_slow1():
    f, g = symbols("f g", cls=Function)
    x, t, x_, t_, d, a, m = symbols("x t x_ t_ d a m")

    # Type 1

    eqs1 = [Eq(f(x).diff(x, 2), 2/x *(x*g(x).diff(x) - g(x))),
           Eq(g(x).diff(x, 2),-2/x *(x*f(x).diff(x) - f(x)))]
    sol1 = [Eq(f(x), C1*x + 2*C2*x*Ci(2*x) - C2*sin(2*x) - 2*C3*x*Si(2*x) - C3*cos(2*x)),
            Eq(g(x), -2*C2*x*Si(2*x) - C2*cos(2*x) - 2*C3*x*Ci(2*x) + C3*sin(2*x) + C4*x)]
    assert dsolve(eqs1) == sol1
    assert checksysodesol(eqs1, sol1) == (True, [0, 0])

