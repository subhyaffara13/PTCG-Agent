
def test_nonlinsolve_basic():
    assert nonlinsolve([],[]) == S.EmptySet
    assert nonlinsolve([],[x, y]) == S.EmptySet

    system = [x, y - x - 5]
    assert nonlinsolve([x],[x, y]) == FiniteSet((0, y))
    assert nonlinsolve(system, [y]) == S.EmptySet
    soln = (ImageSet(Lambda(n, 2*n*pi + pi/2), S.Integers),)
    assert dumeq(nonlinsolve([sin(x) - 1], [x]), FiniteSet(tuple(soln)))
    soln = ((ImageSet(Lambda(n, 2*n*pi + pi), S.Integers), 1),
            (ImageSet(Lambda(n, 2*n*pi), S.Integers), 1))
    assert dumeq(nonlinsolve([sin(x), y - 1], [x, y]), FiniteSet(*soln))
    assert nonlinsolve([x**2 - 1], [x]) == FiniteSet((-1,), (1,))

    soln = FiniteSet((y, y))
    assert nonlinsolve([x - y, 0], x, y) == soln
    assert nonlinsolve([0, x - y], x, y) == soln
    assert nonlinsolve([x - y, x - y], x, y) == soln
    assert nonlinsolve([x, 0], x, y) == FiniteSet((0, y))
    f = Function('f')
    assert nonlinsolve([f(x), 0], f(x), y) == FiniteSet((0, y))
    assert nonlinsolve([f(x), 0], f(x), f(y)) == FiniteSet((0, f(y)))
    A = Indexed('A', x)
    assert nonlinsolve([A, 0], A, y) == FiniteSet((0, y))
    assert nonlinsolve([x**2 -1], [sin(x)]) == FiniteSet((S.EmptySet,))
    assert nonlinsolve([x**2 -1], sin(x)) == FiniteSet((S.EmptySet,))
    assert nonlinsolve([x**2 -1], 1) == FiniteSet((x**2,))
    assert nonlinsolve([x**2 -1], x + y) == FiniteSet((S.EmptySet,))
    assert nonlinsolve([Eq(1, x + y), Eq(1, -x + y - 1), Eq(1, -x + y - 1)], x, y) == FiniteSet(
        (-S.Half, 3*S.Half))

