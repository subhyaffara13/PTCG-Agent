
def test_sinc():
    assert julia_code(sinc(x)) == 'sinc(x / pi)'
    assert julia_code(sinc(x + 3)) == 'sinc((x + 3) / pi)'
    assert julia_code(sinc(pi * (x + 3))) == 'sinc(x + 3)'


def test_sinc():
    assert mcode(sinc(x)) == 'sinc(x/pi)'
    assert mcode(sinc(x + 3)) == 'sinc((x + 3)/pi)'
    assert mcode(sinc(pi*(x + 3))) == 'sinc(x + 3)'


def test_sinc():
    x = Symbol('x')
    lines = [
        '      1 |                          . .                          ',
        '        |                         .   .                         ',
        '        |                                                       ',
        '        |                        .     .                        ',
        '        |                                                       ',
        '        |                       .       .                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                      .         .                      ',
        '        |                                                       ',
        '    0.4 |-------------------------------------------------------',
        '        |                     .           .                     ',
        '        |                                                       ',
        '        |                    .             .                    ',
        '        |                                                       ',
        '        |    .....                                     .....    ',
        '        |  ..     \\         .               .         /     ..  ',
        '        | /        \\                                 /        \\ ',
        '        |/          \\      .                 .      /          \\',
        '        |            \\    /                   \\    /            ',
        '   -0.2 |_______________________________________________________',
        '         -10                        0                          10'
    ]
    # RuntimeWarning: invalid value encountered in double_scalars
    with ignore_warnings(RuntimeWarning):
        assert lines == list(textplot_str(sin(x)/x, -10, 10))


def test_sinc():
    assert isinstance(sinc(x), sinc)

    s = Symbol('s', zero=True)
    assert sinc(s) is S.One
    assert sinc(S.Infinity) is S.Zero
    assert sinc(S.NegativeInfinity) is S.Zero
    assert sinc(S.NaN) is S.NaN
    assert sinc(S.ComplexInfinity) is S.NaN

    n = Symbol('n', integer=True, nonzero=True)
    assert sinc(n*pi) is S.Zero
    assert sinc(-n*pi) is S.Zero
    assert sinc(pi/2) == 2 / pi
    assert sinc(-pi/2) == 2 / pi
    assert sinc(pi*Rational(5, 2)) == 2 / (5*pi)
    assert sinc(pi*Rational(7, 2)) == -2 / (7*pi)

    assert sinc(-x) == sinc(x)

    assert sinc(x).diff(x) == cos(x)/x - sin(x)/x**2
    assert sinc(x).diff(x) == (sin(x)/x).diff(x)
    assert sinc(x).diff(x, x) == (-sin(x) - 2*cos(x)/x + 2*sin(x)/x**2)/x
    assert sinc(x).diff(x, x) == (sin(x)/x).diff(x, x)
    assert limit(sinc(x).diff(x), x, 0) == 0
    assert limit(sinc(x).diff(x, x), x, 0) == -S(1)/3

    # https://github.com/sympy/sympy/issues/11402
    #
    # assert sinc(x).diff(x) == Piecewise(((x*cos(x) - sin(x)) / x**2, Ne(x, 0)), (0, True))
    #
    # assert sinc(x).diff(x).equals(sinc(x).rewrite(sin).diff(x))
    #
    # assert sinc(x).diff(x).subs(x, 0) is S.Zero

    assert sinc(x).series() == 1 - x**2/6 + x**4/120 + O(x**6)

    assert sinc(x).rewrite(jn) == jn(0, x)
    assert sinc(x).rewrite(sin) == Piecewise((sin(x)/x, Ne(x, 0)), (1, True))
    assert sinc(pi, evaluate=False).is_zero is True
    assert sinc(0, evaluate=False).is_zero is False
    assert sinc(n*pi, evaluate=False).is_zero is True
    assert sinc(x).is_zero is None
    xr = Symbol('xr', real=True, nonzero=True)
    assert sinc(x).is_real is None
    assert sinc(xr).is_real is True
    assert sinc(I*xr).is_real is True
    assert sinc(I*100).is_real is True
    assert sinc(x).is_finite is None
    assert sinc(xr).is_finite is True


def test_sinc():
    assert sinc(0) == sincpi(0) == 1
    assert sinc(inf) == sincpi(inf) == 0
    assert sinc(-inf) == sincpi(-inf) == 0
    assert sinc(2).ae(0.45464871341284084770)
    assert sinc(2+3j).ae(0.4463290318402435457-2.7539470277436474940j)
    assert sincpi(2) == 0
    assert sincpi(1.5).ae(-0.212206590789193781)

