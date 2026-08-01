
def test_issue_15265(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    eqn = sin(x)

    p = plot(eqn, xlim=(-S.Pi, S.Pi), ylim=(-1, 1), adaptive=adaptive, n=10)
    p._backend.close()

    p = plot(eqn, xlim=(-1, 1), ylim=(-S.Pi, S.Pi), adaptive=adaptive, n=10)
    p._backend.close()

    p = plot(eqn, xlim=(-1, 1), adaptive=adaptive, n=10,
        ylim=(sympify('-3.14'), sympify('3.14')))
    p._backend.close()

    p = plot(eqn, adaptive=adaptive, n=10,
        xlim=(sympify('-3.14'), sympify('3.14')), ylim=(-1, 1))
    p._backend.close()

    raises(ValueError,
        lambda: plot(eqn, adaptive=adaptive, n=10,
            xlim=(-S.ImaginaryUnit, 1), ylim=(-1, 1)))

    raises(ValueError,
        lambda: plot(eqn, adaptive=adaptive, n=10,
            xlim=(-1, 1), ylim=(-1, S.ImaginaryUnit)))

    raises(ValueError,
        lambda: plot(eqn, adaptive=adaptive, n=10,
            xlim=(S.NegativeInfinity, 1), ylim=(-1, 1)))

    raises(ValueError,
        lambda: plot(eqn, adaptive=adaptive, n=10,
            xlim=(-1, 1), ylim=(-1, S.Infinity)))

