
def test_issue_11045():
    assert integrate(1/(x*sqrt(x**2 - 1)), (x, 1, 2)) == pi/3

    # handle And with Or arguments
    assert Piecewise((1, And(Or(x < 1, x > 3), x < 2)), (0, True)
        ).integrate((x, 0, 3)) == 1

    # hidden false
    assert Piecewise((1, x > 1), (2, x > x + 1), (3, True)
        ).integrate((x, 0, 3)) == 5
    # targetcond is Eq
    assert Piecewise((1, x > 1), (2, Eq(1, x)), (3, True)
        ).integrate((x, 0, 4)) == 6
    # And has Relational needing to be solved
    assert Piecewise((1, And(2*x > x + 1, x < 2)), (0, True)
        ).integrate((x, 0, 3)) == 1
    # Or has Relational needing to be solved
    assert Piecewise((1, Or(2*x > x + 2, x < 1)), (0, True)
        ).integrate((x, 0, 3)) == 2
    # ignore hidden false (handled in canonicalization)
    assert Piecewise((1, x > 1), (2, x > x + 1), (3, True)
        ).integrate((x, 0, 3)) == 5
    # watch for hidden True Piecewise
    assert Piecewise((2, Eq(1 - x, x*(1/x - 1))), (0, True)
        ).integrate((x, 0, 3)) == 6

    # overlapping conditions of targetcond are recognized and ignored;
    # the condition x > 3 will be pre-empted by the first condition
    assert Piecewise((1, Or(x < 1, x > 2)), (2, x > 3), (3, True)
        ).integrate((x, 0, 4)) == 6

    # convert Ne to Or
    assert Piecewise((1, Ne(x, 0)), (2, True)
        ).integrate((x, -1, 1)) == 2

    # no default but well defined
    assert Piecewise((x, (x > 1) & (x < 3)), (1, (x < 4))
        ).integrate((x, 1, 4)) == 5

    p = Piecewise((x, (x > 1) & (x < 3)), (1, (x < 4)))
    nan = Undefined
    i = p.integrate((x, 1, y))
    assert i == Piecewise(
        (y - 1, y < 1),
        (Min(3, y)**2/2 - Min(3, y) + Min(4, y) - S.Half,
            y <= Min(4, y)),
        (nan, True))
    assert p.integrate((x, 1, -1)) == i.subs(y, -1)
    assert p.integrate((x, 1, 4)) == 5
    assert p.integrate((x, 1, 5)) is nan

    # handle Not
    p = Piecewise((1, x > 1), (2, Not(And(x > 1, x< 3))), (3, True))
    assert p.integrate((x, 0, 3)) == 4

    # handle updating of int_expr when there is overlap
    p = Piecewise(
        (1, And(5 > x, x > 1)),
        (2, Or(x < 3, x > 7)),
        (4, x < 8))
    assert p.integrate((x, 0, 10)) == 20

    # And with Eq arg handling
    assert Piecewise((1, x < 1), (2, And(Eq(x, 3), x > 1))
        ).integrate((x, 0, 3)) is S.NaN
    assert Piecewise((1, x < 1), (2, And(Eq(x, 3), x > 1)), (3, True)
        ).integrate((x, 0, 3)) == 7
    assert Piecewise((1, x < 0), (2, And(Eq(x, 3), x < 1)), (3, True)
        ).integrate((x, -1, 1)) == 4
    # middle condition doesn't matter: it's a zero width interval
    assert Piecewise((1, x < 1), (2, Eq(x, 3) & (y < x)), (3, True)
        ).integrate((x, 0, 3)) == 7

