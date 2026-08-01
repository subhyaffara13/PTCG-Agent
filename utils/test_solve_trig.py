
def test_solve_trig():
    assert dumeq(solveset_real(sin(x), x),
        Union(imageset(Lambda(n, 2*pi*n), S.Integers),
              imageset(Lambda(n, 2*pi*n + pi), S.Integers)))

    assert dumeq(solveset_real(sin(x) - 1, x),
        imageset(Lambda(n, 2*pi*n + pi/2), S.Integers))

    assert dumeq(solveset_real(cos(x), x),
        Union(imageset(Lambda(n, 2*pi*n + pi/2), S.Integers),
              imageset(Lambda(n, 2*pi*n + pi*Rational(3, 2)), S.Integers)))

    assert dumeq(solveset_real(sin(x) + cos(x), x),
        Union(imageset(Lambda(n, 2*n*pi + pi*Rational(3, 4)), S.Integers),
              imageset(Lambda(n, 2*n*pi + pi*Rational(7, 4)), S.Integers)))

    assert solveset_real(sin(x)**2 + cos(x)**2, x) == S.EmptySet

    assert dumeq(solveset_complex(cos(x) - S.Half, x),
        Union(imageset(Lambda(n, 2*n*pi + pi*Rational(5, 3)), S.Integers),
              imageset(Lambda(n, 2*n*pi + pi/3), S.Integers)))

    assert dumeq(solveset(sin(y + a) - sin(y), a, domain=S.Reals),
        ConditionSet(a, (S(-1) <= sin(y)) & (sin(y) <= S(1)), Union(
            ImageSet(Lambda(n, 2*n*pi - y + asin(sin(y))), S.Integers),
            ImageSet(Lambda(n, 2*n*pi - y - asin(sin(y)) + pi), S.Integers))))

    assert dumeq(solveset_real(sin(2*x)*cos(x) + cos(2*x)*sin(x)-1, x),
        ImageSet(Lambda(n, n*pi*Rational(2, 3) + pi/6), S.Integers))

    assert dumeq(solveset_real(2*tan(x)*sin(x) + 1, x), Union(
        ImageSet(Lambda(n, 2*n*pi + atan(sqrt(2)*sqrt(-1 + sqrt(17))/
            (1 - sqrt(17))) + pi), S.Integers),
        ImageSet(Lambda(n, 2*n*pi - atan(sqrt(2)*sqrt(-1 + sqrt(17))/
            (1 - sqrt(17))) + pi), S.Integers)))

    assert dumeq(solveset_real(cos(2*x)*cos(4*x) - 1, x),
                            ImageSet(Lambda(n, n*pi), S.Integers))

    assert dumeq(solveset(sin(x/10) + Rational(3, 4)), Union(
        ImageSet(Lambda(n, 20*n*pi - 10*asin(S(3)/4) + 20*pi), S.Integers),
        ImageSet(Lambda(n, 20*n*pi + 10*asin(S(3)/4) + 10*pi), S.Integers)))

    assert dumeq(solveset(cos(x/15) + cos(x/5)), Union(
        ImageSet(Lambda(n, 30*n*pi + 15*pi/2), S.Integers),
        ImageSet(Lambda(n, 30*n*pi + 45*pi/2), S.Integers),
        ImageSet(Lambda(n, 30*n*pi + 75*pi/4), S.Integers),
        ImageSet(Lambda(n, 30*n*pi + 45*pi/4), S.Integers),
        ImageSet(Lambda(n, 30*n*pi + 105*pi/4), S.Integers),
        ImageSet(Lambda(n, 30*n*pi + 15*pi/4), S.Integers)))

    assert dumeq(solveset(sec(sqrt(2)*x/3) + 5), Union(
        ImageSet(Lambda(n, 3*sqrt(2)*(2*n*pi - asec(-5))/2), S.Integers),
        ImageSet(Lambda(n, 3*sqrt(2)*(2*n*pi + asec(-5))/2), S.Integers)))

    assert dumeq(simplify(solveset(tan(pi*x) - cot(pi/2*x))), Union(
        ImageSet(Lambda(n, 4*n + 1), S.Integers),
        ImageSet(Lambda(n, 4*n + 3), S.Integers),
        ImageSet(Lambda(n, 4*n + Rational(7, 3)), S.Integers),
        ImageSet(Lambda(n, 4*n + Rational(5, 3)), S.Integers),
        ImageSet(Lambda(n, 4*n + Rational(11, 3)), S.Integers),
        ImageSet(Lambda(n, 4*n + Rational(1, 3)), S.Integers)))

    assert dumeq(solveset(cos(9*x)), Union(
        ImageSet(Lambda(n, 2*n*pi/9 + pi/18), S.Integers),
        ImageSet(Lambda(n, 2*n*pi/9 + pi/6), S.Integers)))

    assert dumeq(solveset(sin(8*x) + cot(12*x), x, S.Reals), Union(
        ImageSet(Lambda(n, n*pi/2 + pi/8), S.Integers),
        ImageSet(Lambda(n, n*pi/2 + 3*pi/8), S.Integers),
        ImageSet(Lambda(n, n*pi/2 + 5*pi/16), S.Integers),
        ImageSet(Lambda(n, n*pi/2 + 3*pi/16), S.Integers),
        ImageSet(Lambda(n, n*pi/2 + 7*pi/16), S.Integers),
        ImageSet(Lambda(n, n*pi/2 + pi/16), S.Integers)))

    # This is the only remaining solveset test that actually ends up being solved
    # by _solve_trig2(). All others are handled by the improved _solve_trig1.
    assert dumeq(solveset_real(2*cos(x)*cos(2*x) - 1, x),
          Union(ImageSet(Lambda(n, 2*n*pi + 2*atan(sqrt(-2*2**Rational(1, 3)*(67 +
                  9*sqrt(57))**Rational(2, 3) + 8*2**Rational(2, 3) + 11*(67 +
                  9*sqrt(57))**Rational(1, 3))/(3*(67 + 9*sqrt(57))**Rational(1, 6)))), S.Integers),
                  ImageSet(Lambda(n, 2*n*pi - 2*atan(sqrt(-2*2**Rational(1, 3)*(67 +
                  9*sqrt(57))**Rational(2, 3) + 8*2**Rational(2, 3) + 11*(67 +
                  9*sqrt(57))**Rational(1, 3))/(3*(67 + 9*sqrt(57))**Rational(1, 6))) +
                  2*pi), S.Integers)))

    # issue #16870
    assert dumeq(simplify(solveset(sin(x/180*pi) - S.Half, x, S.Reals)), Union(
        ImageSet(Lambda(n, 360*n + 150), S.Integers),
        ImageSet(Lambda(n, 360*n + 30), S.Integers)))

