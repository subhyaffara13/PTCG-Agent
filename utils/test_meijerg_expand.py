
def test_meijerg_expand():
    from sympy.simplify.gammasimp import gammasimp
    from sympy.simplify.simplify import simplify
    # from mpmath docs
    assert hyperexpand(meijerg([[], []], [[0], []], -z)) == exp(z)

    assert hyperexpand(meijerg([[1, 1], []], [[1], [0]], z)) == \
        log(z + 1)
    assert hyperexpand(meijerg([[1, 1], []], [[1], [1]], z)) == \
        z/(z + 1)
    assert hyperexpand(meijerg([[], []], [[S.Half], [0]], (z/2)**2)) \
        == sin(z)/sqrt(pi)
    assert hyperexpand(meijerg([[], []], [[0], [S.Half]], (z/2)**2)) \
        == cos(z)/sqrt(pi)
    assert can_do_meijer([], [a], [a - 1, a - S.Half], [])
    assert can_do_meijer([], [], [a/2], [-a/2], False)  # branches...
    assert can_do_meijer([a], [b], [a], [b, a - 1])

    # wikipedia
    assert hyperexpand(meijerg([1], [], [], [0], z)) == \
        Piecewise((0, abs(z) < 1), (1, abs(1/z) < 1),
                 (meijerg([1], [], [], [0], z), True))
    assert hyperexpand(meijerg([], [1], [0], [], z)) == \
        Piecewise((1, abs(z) < 1), (0, abs(1/z) < 1),
                 (meijerg([], [1], [0], [], z), True))

    # The Special Functions and their Approximations
    assert can_do_meijer([], [], [a + b/2], [a, a - b/2, a + S.Half])
    assert can_do_meijer(
        [], [], [a], [b], False)  # branches only agree for small z
    assert can_do_meijer([], [S.Half], [a], [-a])
    assert can_do_meijer([], [], [a, b], [])
    assert can_do_meijer([], [], [a, b], [])
    assert can_do_meijer([], [], [a, a + S.Half], [b, b + S.Half])
    assert can_do_meijer([], [], [a, -a], [0, S.Half], False)  # dito
    assert can_do_meijer([], [], [a, a + S.Half, b, b + S.Half], [])
    assert can_do_meijer([S.Half], [], [0], [a, -a])
    assert can_do_meijer([S.Half], [], [a], [0, -a], False)  # dito
    assert can_do_meijer([], [a - S.Half], [a, b], [a - S.Half], False)
    assert can_do_meijer([], [a + S.Half], [a + b, a - b, a], [], False)
    assert can_do_meijer([a + S.Half], [], [b, 2*a - b, a], [], False)

    # This for example is actually zero.
    assert can_do_meijer([], [], [], [a, b])

    # Testing a bug:
    assert hyperexpand(meijerg([0, 2], [], [], [-1, 1], z)) == \
        Piecewise((0, abs(z) < 1),
                  (z*(1 - 1/z**2)/2, abs(1/z) < 1),
                  (meijerg([0, 2], [], [], [-1, 1], z), True))

    # Test that the simplest possible answer is returned:
    assert gammasimp(simplify(hyperexpand(
        meijerg([1], [1 - a], [-a/2, -a/2 + S.Half], [], 1/z)))) == \
        -2*sqrt(pi)*(sqrt(z + 1) + 1)**a/a

    # Test that hyper is returned
    assert hyperexpand(meijerg([1], [], [a], [0, 0], z)) == hyper(
        (a,), (a + 1, a + 1), z*exp_polar(I*pi))*z**a*gamma(a)/gamma(a + 1)**2

    # Test place option
    f = meijerg(((0, 1), ()), ((S.Half,), (0,)), z**2)
    assert hyperexpand(f) == sqrt(pi)/sqrt(1 + z**(-2))
    assert hyperexpand(f, place=0) == sqrt(pi)*z/sqrt(z**2 + 1)

