
def test_solve_args():
    # equation container, issue 5113
    ans = {x: -3, y: 1}
    eqs = (x + 5*y - 2, -3*x + 6*y - 15)
    assert all(solve(container(eqs), x, y) == ans for container in
        (tuple, list, set, frozenset))
    assert solve(Tuple(*eqs), x, y) == ans
    # implicit symbol to solve for
    assert set(solve(x**2 - 4)) == {S(2), -S(2)}
    assert solve([x + y - 3, x - y - 5]) == {x: 4, y: -1}
    assert solve(x - exp(x), x, implicit=True) == [exp(x)]
    # no symbol to solve for
    assert solve(42) == solve(42, x) == []
    assert solve([1, 2]) == []
    assert solve([sqrt(2)],[x]) == []
    # duplicate symbols raises
    raises(ValueError, lambda: solve((x - 3, y + 2), x, y, x))
    raises(ValueError, lambda: solve(x, x, x))
    # no error in exclude
    assert solve(x, x, exclude=[y, y]) == [0]
    # duplicate symbols raises
    raises(ValueError, lambda: solve((x - 3, y + 2), x, y, x))
    raises(ValueError, lambda: solve(x, x, x))
    # no error in exclude
    assert solve(x, x, exclude=[y, y]) == [0]
    # unordered symbols
    # only 1
    assert solve(y - 3, {y}) == [3]
    # more than 1
    assert solve(y - 3, {x, y}) == [{y: 3}]
    # multiple symbols: take the first linear solution+
    # - return as tuple with values for all requested symbols
    assert solve(x + y - 3, [x, y]) == [(3 - y, y)]
    # - unless dict is True
    assert solve(x + y - 3, [x, y], dict=True) == [{x: 3 - y}]
    # - or no symbols are given
    assert solve(x + y - 3) == [{x: 3 - y}]
    # multiple symbols might represent an undetermined coefficients system
    assert solve(a + b*x - 2, [a, b]) == {a: 2, b: 0}
    assert solve((a + b)*x + b - c, [a, b]) == {a: -c, b: c}
    eq = a*x**2 + b*x + c - ((x - h)**2 + 4*p*k)/4/p
    # - check that flags are obeyed
    sol = solve(eq, [h, p, k], exclude=[a, b, c])
    assert sol == {h: -b/(2*a), k: (4*a*c - b**2)/(4*a), p: 1/(4*a)}
    assert solve(eq, [h, p, k], dict=True) == [sol]
    assert solve(eq, [h, p, k], set=True) == \
        ([h, p, k], {(-b/(2*a), 1/(4*a), (4*a*c - b**2)/(4*a))})
    # issue 23889 - polysys not simplified
    assert solve(eq, [h, p, k], exclude=[a, b, c], simplify=False) == \
        {h: -b/(2*a), k: (4*a*c - b**2)/(4*a), p: 1/(4*a)}
    # but this only happens when system has a single solution
    args = (a + b)*x - b**2 + 2, a, b
    assert solve(*args) == [((b**2 - b*x - 2)/x, b)]
    # and if the system has a solution; the following doesn't so
    # an algebraic solution is returned
    assert solve(a*x + b**2/(x + 4) - 3*x - 4/x, a, b, dict=True) == \
        [{a: (-b**2*x + 3*x**3 + 12*x**2 + 4*x + 16)/(x**2*(x + 4))}]
    # failed single equation
    assert solve(1/(1/x - y + exp(y))) == []
    raises(
        NotImplementedError, lambda: solve(exp(x) + sin(x) + exp(y) + sin(y)))
    # failed system
    # --  when no symbols given, 1 fails
    assert solve([y, exp(x) + x]) == [{x: -LambertW(1), y: 0}]
    #     both fail
    assert solve(
        (exp(x) - x, exp(y) - y)) == [{x: -LambertW(-1), y: -LambertW(-1)}]
    # --  when symbols given
    assert solve([y, exp(x) + x], x, y) == [(-LambertW(1), 0)]
    # symbol is a number
    assert solve(x**2 - pi, pi) == [x**2]
    # no equations
    assert solve([], [x]) == []
    # nonlinear system
    assert solve((x**2 - 4, y - 2), x, y) == [(-2, 2), (2, 2)]
    assert solve((x**2 - 4, y - 2), y, x) == [(2, -2), (2, 2)]
    assert solve((x**2 - 4 + z, y - 2 - z), a, z, y, x, set=True
        ) == ([a, z, y, x], {
        (a, z, z + 2, -sqrt(4 - z)),
        (a, z, z + 2, sqrt(4 - z))})
    # overdetermined system
    # - nonlinear
    assert solve([(x + y)**2 - 4, x + y - 2]) == [{x: -y + 2}]
    # - linear
    assert solve((x + y - 2, 2*x + 2*y - 4)) == {x: -y + 2}
    # When one or more args are Boolean
    assert solve(Eq(x**2, 0.0)) == [0.0]  # issue 19048
    assert solve([True, Eq(x, 0)], [x], dict=True) == [{x: 0}]
    assert solve([Eq(x, x), Eq(x, 0), Eq(x, x+1)], [x], dict=True) == []
    assert not solve([Eq(x, x+1), x < 2], x)
    assert solve([Eq(x, 0), x+1<2]) == Eq(x, 0)
    assert solve([Eq(x, x), Eq(x, x+1)], x) == []
    assert solve(True, x) == []
    assert solve([x - 1, False], [x], set=True) == ([], set())
    assert solve([-y*(x + y - 1)/2, (y - 1)/x/y + 1/y],
        set=True, check=False) == ([x, y], {(1 - y, y), (x, 0)})
    # ordering should be canonical, fastest to order by keys instead
    # of by size
    assert list(solve((y - 1, x - sqrt(3)*z)).keys()) == [x, y]
    # as set always returns as symbols, set even if no solution
    assert solve([x - 1, x], (y, x), set=True) == ([y, x], set())
    assert solve([x - 1, x], {y, x}, set=True) == ([x, y], set())

