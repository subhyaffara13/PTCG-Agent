import re

def test_complex():
    a, b = symbols('a,b', real=True)
    z = a + b*I
    for func in [sinh, cosh, tanh, coth, sech, csch]:
        assert func(z).conjugate() == func(a - b*I)
    for deep in [True, False]:
        assert sinh(z).expand(
            complex=True, deep=deep) == sinh(a)*cos(b) + I*cosh(a)*sin(b)
        assert cosh(z).expand(
            complex=True, deep=deep) == cosh(a)*cos(b) + I*sinh(a)*sin(b)
        assert tanh(z).expand(complex=True, deep=deep) == sinh(a)*cosh(
            a)/(cos(b)**2 + sinh(a)**2) + I*sin(b)*cos(b)/(cos(b)**2 + sinh(a)**2)
        assert coth(z).expand(complex=True, deep=deep) == sinh(a)*cosh(
            a)/(sin(b)**2 + sinh(a)**2) - I*sin(b)*cos(b)/(sin(b)**2 + sinh(a)**2)
        assert csch(z).expand(complex=True, deep=deep) == cos(b) * sinh(a) / (sin(b)**2\
            *cosh(a)**2 + cos(b)**2 * sinh(a)**2) - I*sin(b) * cosh(a) / (sin(b)**2\
            *cosh(a)**2 + cos(b)**2 * sinh(a)**2)
        assert sech(z).expand(complex=True, deep=deep) == cos(b) * cosh(a) / (sin(b)**2\
            *sinh(a)**2 + cos(b)**2 * cosh(a)**2) - I*sin(b) * sinh(a) / (sin(b)**2\
            *sinh(a)**2 + cos(b)**2 * cosh(a)**2)


def test_complex():
    a = Symbol("a", real=True)
    b = Symbol("b", real=True)
    e = (a + I*b)*(a - I*b)
    assert e.expand() == a**2 + b**2
    assert sqrt(I) == Pow(I, S.Half)


def test_complex():
    a, b, c = map(Symbol, 'abc')
    x, y = map(Wild, 'xy')

    assert (1 + I).match(x + I) == {x: 1}
    assert (a + I).match(x + I) == {x: a}
    assert (2*I).match(x*I) == {x: 2}
    assert (a*I).match(x*I) == {x: a}
    assert (a*I).match(x*y) == {x: I, y: a}
    assert (2*I).match(x*y) == {x: 2, y: I}
    assert (a + b*I).match(x + y*I) == {x: a, y: b}


def test_complex():
    assert ask(Q.complex(x)) is None
    assert ask(Q.complex(x), Q.complex(x)) is True
    assert ask(Q.complex(x), Q.complex(y)) is None
    assert ask(Q.complex(x), ~Q.complex(x)) is False
    assert ask(Q.complex(x), Q.real(x)) is True
    assert ask(Q.complex(x), ~Q.real(x)) is None
    assert ask(Q.complex(x), Q.rational(x)) is True
    assert ask(Q.complex(x), Q.irrational(x)) is True
    assert ask(Q.complex(x), Q.positive(x)) is True
    assert ask(Q.complex(x), Q.imaginary(x)) is True
    assert ask(Q.complex(x), Q.algebraic(x)) is True

    # a+b
    assert ask(Q.complex(x + 1), Q.complex(x)) is True
    assert ask(Q.complex(x + 1), Q.real(x)) is True
    assert ask(Q.complex(x + 1), Q.rational(x)) is True
    assert ask(Q.complex(x + 1), Q.irrational(x)) is True
    assert ask(Q.complex(x + 1), Q.imaginary(x)) is True
    assert ask(Q.complex(x + 1), Q.integer(x)) is True
    assert ask(Q.complex(x + 1), Q.even(x)) is True
    assert ask(Q.complex(x + 1), Q.odd(x)) is True
    assert ask(Q.complex(x + y), Q.complex(x) & Q.complex(y)) is True
    assert ask(Q.complex(x + y), Q.real(x) & Q.imaginary(y)) is True

    # a*x +b
    assert ask(Q.complex(2*x + 1), Q.complex(x)) is True
    assert ask(Q.complex(2*x + 1), Q.real(x)) is True
    assert ask(Q.complex(2*x + 1), Q.positive(x)) is True
    assert ask(Q.complex(2*x + 1), Q.rational(x)) is True
    assert ask(Q.complex(2*x + 1), Q.irrational(x)) is True
    assert ask(Q.complex(2*x + 1), Q.imaginary(x)) is True
    assert ask(Q.complex(2*x + 1), Q.integer(x)) is True
    assert ask(Q.complex(2*x + 1), Q.even(x)) is True
    assert ask(Q.complex(2*x + 1), Q.odd(x)) is True

    # x**2
    assert ask(Q.complex(x**2), Q.complex(x)) is True
    assert ask(Q.complex(x**2), Q.real(x)) is True
    assert ask(Q.complex(x**2), Q.positive(x)) is True
    assert ask(Q.complex(x**2), Q.rational(x)) is True
    assert ask(Q.complex(x**2), Q.irrational(x)) is True
    assert ask(Q.complex(x**2), Q.imaginary(x)) is True
    assert ask(Q.complex(x**2), Q.integer(x)) is True
    assert ask(Q.complex(x**2), Q.even(x)) is True
    assert ask(Q.complex(x**2), Q.odd(x)) is True

    # 2**x
    assert ask(Q.complex(2**x), Q.complex(x)) is True
    assert ask(Q.complex(2**x), Q.real(x)) is True
    assert ask(Q.complex(2**x), Q.positive(x)) is True
    assert ask(Q.complex(2**x), Q.rational(x)) is True
    assert ask(Q.complex(2**x), Q.irrational(x)) is True
    assert ask(Q.complex(2**x), Q.imaginary(x)) is True
    assert ask(Q.complex(2**x), Q.integer(x)) is True
    assert ask(Q.complex(2**x), Q.even(x)) is True
    assert ask(Q.complex(2**x), Q.odd(x)) is True
    assert ask(Q.complex(x**y), Q.complex(x) & Q.complex(y)) is True

    # trigonometric expressions
    assert ask(Q.complex(sin(x))) is True
    assert ask(Q.complex(sin(2*x + 1))) is True
    assert ask(Q.complex(cos(x))) is True
    assert ask(Q.complex(cos(2*x + 1))) is True

    # exponential
    assert ask(Q.complex(exp(x))) is True
    assert ask(Q.complex(exp(x))) is True

    # Q.complexes
    assert ask(Q.complex(Abs(x))) is True
    assert ask(Q.complex(re(x))) is True
    assert ask(Q.complex(im(x))) is True


def test_complex():
    assert refine(re(1/(x + I*y)), Q.real(x) & Q.real(y)) == \
        x/(x**2 + y**2)
    assert refine(im(1/(x + I*y)), Q.real(x) & Q.real(y)) == \
        -y/(x**2 + y**2)
    assert refine(re((w + I*x) * (y + I*z)), Q.real(w) & Q.real(x) & Q.real(y)
        & Q.real(z)) == w*y - x*z
    assert refine(im((w + I*x) * (y + I*z)), Q.real(w) & Q.real(x) & Q.real(y)
        & Q.real(z)) == w*z + x*y


def test_complex():
    def func(z):
        return z**2 - 1 + 2j
    x0 = 2.0j

    ftol = 1e-4
    sol = root(func, x0, tol=ftol, method='DF-SANE')

    assert_(sol.success)

    f0 = np.linalg.norm(func(x0))
    fx = np.linalg.norm(func(sol.x))
    assert_(fx <= ftol*f0)


def test_complex(method):
    # Complex-valued data deprecated
    x = np.arange(0., 11.)
    y = np.array([0., 2., 1., 3., 2., 6., 5.5, 5.5, 2.7, 5.1, 3.])
    y = y - 2j*y
    msg = "real values"
    with pytest.raises(ValueError, match=msg):
        method(x, y)

    def test_concurrency(self):
        # Check that no segfaults appear with concurrent access to Akima1D
        x = np.linspace(-5, 5, 11)
        y = x**2
        x_ext = np.linspace(-10, 10, 17)
        ak = Akima1DInterpolator(x, y, extrapolate=True)

        def worker_fn(_, ak, x_ext):
            ak(x_ext)

        _run_concurrent_barrier(10, worker_fn, ak, x_ext)


def test_complex():
    x = [1, 2, 3, 4]
    y = [1, 2, 1j, 3]

    for ip in [KroghInterpolator, BarycentricInterpolator, CubicSpline]:
        p = ip(x, y)
        xp_assert_close(p(x), np.asarray(y))

    dydx = [0, -1j, 2, 3j]
    p = CubicHermiteSpline(x, y, dydx)
    xp_assert_close(p(x), np.asarray(y))
    xp_assert_close(p(x, 1), np.asarray(dydx))


def test_complex():
    # The test is essentially the same as test_no_params, but boundary
    # conditions are turned into complex.
    x = np.linspace(0, 1, 5)
    x_test = np.linspace(0, 1, 100)
    y = np.zeros((2, x.shape[0]), dtype=complex)
    for fun_jac in [None, exp_fun_jac]:
        for bc_jac in [None, exp_bc_jac]:
            sol = solve_bvp(exp_fun, exp_bc_complex, x, y, fun_jac=fun_jac,
                            bc_jac=bc_jac)

            assert_equal(sol.status, 0)
            assert_(sol.success)

            sol_test = sol.sol(x_test)

            assert_allclose(sol_test[0].real, exp_sol(x_test), atol=1e-5)
            assert_allclose(sol_test[0].imag, exp_sol(x_test), atol=1e-5)

            f_test = exp_fun(x_test, sol_test)
            r = sol.sol(x_test, 1) - f_test
            rel_res = r / (1 + np.abs(f_test))
            norm_res = np.sum(np.real(rel_res * np.conj(rel_res)),
                              axis=0) ** 0.5
            assert_(np.all(norm_res < 1e-3))

            assert_(np.all(sol.rms_residuals < 1e-3))
            assert_allclose(sol.sol(sol.x), sol.y, rtol=1e-10, atol=1e-10)
            assert_allclose(sol.sol(sol.x, 1), sol.yp, rtol=1e-10, atol=1e-10)


def test_complex(transform, dtype):
    y = transform(1j*np.arange(5, dtype=dtype))
    x = 1j*transform(np.arange(5))
    assert_array_almost_equal(x, y)


def test_complex(install_temp):
    from checks import inc2_cfloat_struct

    arr = np.array([0, 10 + 10j], dtype="F")
    inc2_cfloat_struct(arr)
    assert arr[1] == (12 + 12j)

