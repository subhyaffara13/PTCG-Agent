
def test_solve_inequalities():
    x = Symbol('x')
    sol = And(S.Zero < x, x < oo)
    assert solve(x + 1 > 1) == sol
    assert solve([x + 1 > 1]) == sol
    assert solve([x + 1 > 1], x) == sol
    assert solve([x + 1 > 1], [x]) == sol

    system = [Lt(x**2 - 2, 0), Gt(x**2 - 1, 0)]
    assert solve(system) == \
        And(Or(And(Lt(-sqrt(2), x), Lt(x, -1)),
               And(Lt(1, x), Lt(x, sqrt(2)))), Eq(0, 0))

    x = Symbol('x', real=True)
    system = [Lt(x**2 - 2, 0), Gt(x**2 - 1, 0)]
    assert solve(system) == \
        Or(And(Lt(-sqrt(2), x), Lt(x, -1)), And(Lt(1, x), Lt(x, sqrt(2))))

    # issues 6627, 3448
    assert solve((x - 3)/(x - 2) < 0, x) == And(Lt(2, x), Lt(x, 3))
    assert solve(x/(x + 1) > 1, x) == And(Lt(-oo, x), Lt(x, -1))

    assert solve(sin(x) > S.Half) == And(pi/6 < x, x < pi*Rational(5, 6))

    assert solve(Eq(False, x < 1)) == (S.One <= x) & (x < oo)
    assert solve(Eq(True, x < 1)) == (-oo < x) & (x < 1)
    assert solve(Eq(x < 1, False)) == (S.One <= x) & (x < oo)
    assert solve(Eq(x < 1, True)) == (-oo < x) & (x < 1)

    assert solve(Eq(False, x)) == False
    assert solve(Eq(0, x)) == [0]
    assert solve(Eq(True, x)) == True
    assert solve(Eq(1, x)) == [1]
    assert solve(Eq(False, ~x)) == True
    assert solve(Eq(True, ~x)) == False
    assert solve(Ne(True, x)) == False
    assert solve(Ne(1, x)) == (x > -oo) & (x < oo) & Ne(x, 1)

