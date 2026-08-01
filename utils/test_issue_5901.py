
def test_issue_5901():
    f, g, h = map(Function, 'fgh')
    a = Symbol('a')
    D = Derivative(f(x), x)
    G = Derivative(g(a), a)
    assert solve(f(x) + f(x).diff(x), f(x)) == \
        [-D]
    assert solve(f(x) - 3, f(x)) == \
        [3]
    assert solve(f(x) - 3*f(x).diff(x), f(x)) == \
        [3*D]
    assert solve([f(x) - 3*f(x).diff(x)], f(x)) == \
        {f(x): 3*D}
    assert solve([f(x) - 3*f(x).diff(x), f(x)**2 - y + 4], f(x), y) == \
        [(3*D, 9*D**2 + 4)]
    assert solve(-f(a)**2*g(a)**2 + f(a)**2*h(a)**2 + g(a).diff(a),
                h(a), g(a), set=True) == \
        ([h(a), g(a)], {
        (-sqrt(f(a)**2*g(a)**2 - G)/f(a), g(a)),
        (sqrt(f(a)**2*g(a)**2 - G)/f(a), g(a))}), solve(-f(a)**2*g(a)**2 + f(a)**2*h(a)**2 + g(a).diff(a),
                h(a), g(a), set=True)
    args = [[f(x).diff(x, 2)*(f(x) + g(x)), 2 - g(x)**2], f(x), g(x)]
    assert solve(*args, set=True)[1] == \
        {(-sqrt(2), sqrt(2)), (sqrt(2), -sqrt(2))}
    eqs = [f(x)**2 + g(x) - 2*f(x).diff(x), g(x)**2 - 4]
    assert solve(eqs, f(x), g(x), set=True) == \
        ([f(x), g(x)], {
        (-sqrt(2*D - 2), S(2)),
        (sqrt(2*D - 2), S(2)),
        (-sqrt(2*D + 2), -S(2)),
        (sqrt(2*D + 2), -S(2))})

    # the underlying problem was in solve_linear that was not masking off
    # anything but a Mul or Add; it now raises an error if it gets anything
    # but a symbol and solve handles the substitutions necessary so solve_linear
    # won't make this error
    raises(
        ValueError, lambda: solve_linear(f(x) + f(x).diff(x), symbols=[f(x)]))
    assert solve_linear(f(x) + f(x).diff(x), symbols=[x]) == \
        (f(x) + Derivative(f(x), x), 1)
    assert solve_linear(f(x) + Integral(x, (x, y)), symbols=[x]) == \
        (f(x) + Integral(x, (x, y)), 1)
    assert solve_linear(f(x) + Integral(x, (x, y)) + x, symbols=[x]) == \
        (x + f(x) + Integral(x, (x, y)), 1)
    assert solve_linear(f(y) + Integral(x, (x, y)) + x, symbols=[x]) == \
        (x, -f(y) - Integral(x, (x, y)))
    assert solve_linear(x - f(x)/a + (f(x) - 1)/a, symbols=[x]) == \
        (x, 1/a)
    assert solve_linear(x + Derivative(2*x, x)) == \
        (x, -2)
    assert solve_linear(x + Integral(x, y), symbols=[x]) == \
        (x, 0)
    assert solve_linear(x + Integral(x, y) - 2, symbols=[x]) == \
        (x, 2/(y + 1))

    assert set(solve(x + exp(x)**2, exp(x))) == \
        {-sqrt(-x), sqrt(-x)}
    assert solve(x + exp(x), x, implicit=True) == \
        [-exp(x)]
    assert solve(cos(x) - sin(x), x, implicit=True) == []
    assert solve(x - sin(x), x, implicit=True) == \
        [sin(x)]
    assert solve(x**2 + x - 3, x, implicit=True) == \
        [-x**2 + 3]
    assert solve(x**2 + x - 3, x**2, implicit=True) == \
        [-x + 3]

