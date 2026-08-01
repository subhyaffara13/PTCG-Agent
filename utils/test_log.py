
def test_log():
    # https://github.com/sympy/sympy/issues/21598
    a, b, c = symbols('a b c', positive=True)
    A = log(a/b) - (log(a) - log(b))
    assert A.limit(a, oo) == 0
    assert (A * c).limit(a, oo) == 0

    tau, x = symbols('tau x', positive=True)
    # The value of manualintegrate in the issue
    expr = tau**2*((tau - 1)*(tau + 1)*log(x + 1)/(tau**2 + 1)**2 + 1/((tau**2\
            + 1)*(x + 1)) - (-2*tau*atan(x/tau) + (tau**2/2 - 1/2)*log(tau**2\
            + x**2))/(tau**2 + 1)**2)
    assert limit(expr, x, oo) == pi*tau**3/(tau**2 + 1)**2


def test_log():
    R, x = ring('x', QQ)
    p = 1 + x
    assert rs_log(p, x, 4) == x - x**2/2 + x**3/3
    p = 1 + x +2*x**2/3
    p1 = rs_log(p, x, 9)
    assert p1 == -17*x**8/648 + 13*x**7/189 - 11*x**6/162 - x**5/45 + \
      7*x**4/36 - x**3/3 + x**2/6 + x
    p2 = rs_series_inversion(p, x, 9)
    p3 = rs_log(p2, x, 9)
    assert p3 == -p1

    R, x, y = ring('x, y', QQ)
    p = 1 + x + 2*y*x**2
    p1 = rs_log(p, x, 6)
    assert p1 == (4*x**5*y**2 - 2*x**5*y - 2*x**4*y**2 + x**5/5 + 2*x**4*y -
                  x**4/4 - 2*x**3*y + x**3/3 + 2*x**2*y - x**2/2 + x)

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', EX)
    assert rs_log(x + a, x, 5) == -EX(1/(4*a**4))*x**4 + EX(1/(3*a**3))*x**3 \
        - EX(1/(2*a**2))*x**2 + EX(1/a)*x + EX(log(a))
    assert rs_log(x + x**2*y + a, x, 4) == -EX(a**(-2))*x**3*y + \
        EX(1/(3*a**3))*x**3 + EX(1/a)*x**2*y - EX(1/(2*a**2))*x**2 + \
        EX(1/a)*x + EX(log(a))

    p = x + x**2 + 3
    assert rs_log(p, x, 10).compose(x, 5) == EX(log(3) + Rational(19281291595, 9920232))


def test_log():
    a = log(interval(1, 2))
    assert a.start == 0
    assert a.end == np.log(2)
    a = log(interval(-1, 1))
    assert a.is_valid is None
    a = log(interval(-3, -1))
    assert a.is_valid is False
    a = log(-3)
    assert a.is_valid is False
    a = log(2)
    assert a.start == np.log(2)
    assert a.end == np.log(2)


def test_log():
    l = Symbol('lamda')

    m = Matrix.jordan_block(1, l)
    assert m._eval_matrix_log_jblock() == Matrix([[log(l)]])

    m = Matrix.jordan_block(4, l)
    assert m._eval_matrix_log_jblock() == \
        Matrix(
            [
                [log(l), 1/l, -1/(2*l**2), 1/(3*l**3)],
                [0, log(l), 1/l, -1/(2*l**2)],
                [0, 0, log(l), 1/l],
                [0, 0, 0, log(l)]
            ]
        )

    m = Matrix(
        [[0, 0, 1],
        [0, 0, 0],
        [-1, 0, 0]]
    )
    raises(MatrixError, lambda: m.log())


def test_log():
    l = Symbol('lamda')

    m = Matrix.jordan_block(1, l)
    assert m._eval_matrix_log_jblock() == Matrix([[log(l)]])

    m = Matrix.jordan_block(4, l)
    assert m._eval_matrix_log_jblock() == \
        Matrix(
            [
                [log(l), 1/l, -1/(2*l**2), 1/(3*l**3)],
                [0, log(l), 1/l, -1/(2*l**2)],
                [0, 0, log(l), 1/l],
                [0, 0, 0, log(l)]
            ]
        )

    m = Matrix(
        [[0, 0, 1],
        [0, 0, 0],
        [-1, 0, 0]]
    )
    raises(MatrixError, lambda: m.log())


def test_log(mocker, stdout_mock):
    cli.log('msg')
    cli.log('msg', indent=1)
    cli.log('{0} + 1', 2)
    cli.log('{0} + 1', 2, noformat=True)

    stdout_mock.assert_has_calls(
        [
            mocker.call('msg\n'),
            mocker.call('    msg\n'),
            mocker.call('2 + 1\n'),
            mocker.call('{0} + 1\n'),
        ]
    )
    assert stdout_mock.call_count == 4


def test_log():
    mp.dps = 15
    assert log(1) == 0
    for x in [0.5, 1.5, 2.0, 3.0, 100, 10**50, 1e-50]:
        assert log(x).ae(math.log(x))
        assert log(x, x) == 1
    assert log(1024, 2) == 10
    assert log(10**1234, 10) == 1234
    assert log(2+2j).ae(cmath.log(2+2j))
    # Accuracy near 1
    assert (log(0.6+0.8j).real*10**17).ae(2.2204460492503131)
    assert (log(0.6-0.8j).real*10**17).ae(2.2204460492503131)
    assert (log(0.8-0.6j).real*10**17).ae(2.2204460492503131)
    assert (log(1+1e-8j).real*10**16).ae(0.5)
    assert (log(1-1e-8j).real*10**16).ae(0.5)
    assert (log(-1+1e-8j).real*10**16).ae(0.5)
    assert (log(-1-1e-8j).real*10**16).ae(0.5)
    assert (log(1j+1e-8).real*10**16).ae(0.5)
    assert (log(1j-1e-8).real*10**16).ae(0.5)
    assert (log(-1j+1e-8).real*10**16).ae(0.5)
    assert (log(-1j-1e-8).real*10**16).ae(0.5)
    assert (log(1+1e-40j).real*10**80).ae(0.5)
    assert (log(1j+1e-40).real*10**80).ae(0.5)
    # Huge
    assert log(ldexp(1.234,10**20)).ae(log(2)*1e20)
    assert log(ldexp(1.234,10**200)).ae(log(2)*1e200)
    # Some special values
    assert log(mpc(0,0)) == mpc(-inf,0)
    assert isnan(log(mpc(nan,0)).real)
    assert isnan(log(mpc(nan,0)).imag)
    assert isnan(log(mpc(0,nan)).real)
    assert isnan(log(mpc(0,nan)).imag)
    assert isnan(log(mpc(nan,1)).real)
    assert isnan(log(mpc(nan,1)).imag)
    assert isnan(log(mpc(1,nan)).real)
    assert isnan(log(mpc(1,nan)).imag)

