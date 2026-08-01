
def test_scipy_fns():
    if not scipy:
        skip("scipy not installed")

    single_arg_sympy_fns = [Ei, erf, erfc, factorial, gamma, loggamma, digamma, Si, Ci]
    single_arg_scipy_fns = [scipy.special.expi, scipy.special.erf, scipy.special.erfc,
        scipy.special.factorial, scipy.special.gamma, scipy.special.gammaln,
                            scipy.special.psi, scipy.special.sici, scipy.special.sici]
    numpy.random.seed(0)
    for (sympy_fn, scipy_fn) in zip(single_arg_sympy_fns, single_arg_scipy_fns):
        f = lambdify(x, sympy_fn(x), modules="scipy")
        for i in range(20):
            tv = numpy.random.uniform(-10, 10) + 1j*numpy.random.uniform(-5, 5)
            # SciPy thinks that factorial(z) is 0 when re(z) < 0 and
            # does not support complex numbers.
            # SymPy does not think so.
            if sympy_fn == factorial:
                tv = numpy.abs(tv)
            # SciPy supports gammaln for real arguments only,
            # and there is also a branch cut along the negative real axis
            if sympy_fn == loggamma:
                tv = numpy.abs(tv)
            # SymPy's digamma evaluates as polygamma(0, z)
            # which SciPy supports for real arguments only
            if sympy_fn == digamma:
                tv = numpy.real(tv)
            sympy_result = sympy_fn(tv).evalf()
            scipy_result = scipy_fn(tv)
            # SciPy's sici returns a tuple with both Si and Ci present in it
            # which needs to be unpacked
            if sympy_fn == Si:
                scipy_result = scipy_fn(tv)[0]
            if sympy_fn == Ci:
                scipy_result = scipy_fn(tv)[1]
            assert abs(f(tv) - sympy_result) < 1e-13*(1 + abs(sympy_result))
            assert abs(f(tv) - scipy_result) < 1e-13*(1 + abs(sympy_result))

    double_arg_sympy_fns = [RisingFactorial, besselj, bessely, besseli,
                            besselk, polygamma]
    double_arg_scipy_fns = [scipy.special.poch, scipy.special.jv,
                            scipy.special.yv, scipy.special.iv, scipy.special.kv, scipy.special.polygamma]
    for (sympy_fn, scipy_fn) in zip(double_arg_sympy_fns, double_arg_scipy_fns):
        f = lambdify((x, y), sympy_fn(x, y), modules="scipy")
        for i in range(20):
            # SciPy supports only real orders of Bessel functions
            tv1 = numpy.random.uniform(-10, 10)
            tv2 = numpy.random.uniform(-10, 10) + 1j*numpy.random.uniform(-5, 5)
            # SciPy requires a real valued 2nd argument for: poch, polygamma
            if sympy_fn in (RisingFactorial, polygamma):
                tv2 = numpy.real(tv2)
            if sympy_fn == polygamma:
                tv1 = abs(int(tv1))  # first argument to polygamma must be a non-negative integer.
            sympy_result = sympy_fn(tv1, tv2).evalf()
            assert abs(f(tv1, tv2) - sympy_result) < 1e-13*(1 + abs(sympy_result))
            assert abs(f(tv1, tv2) - scipy_fn(tv1, tv2)) < 1e-13*(1 + abs(sympy_result))

