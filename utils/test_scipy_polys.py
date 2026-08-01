
def test_scipy_polys():
    if not scipy:
        skip("scipy not installed")
    numpy.random.seed(0)

    params = symbols('n k a b')
    # list polynomials with the number of parameters
    polys = [
        (chebyshevt, 1),
        (chebyshevu, 1),
        (legendre, 1),
        (hermite, 1),
        (laguerre, 1),
        (gegenbauer, 2),
        (assoc_legendre, 2),
        (assoc_laguerre, 2),
        (jacobi, 3)
    ]

    msg = \
        "The random test of the function {func} with the arguments " \
        "{args} had failed because the SymPy result {sympy_result} " \
        "and SciPy result {scipy_result} had failed to converge " \
        "within the tolerance {tol} " \
        "(Actual absolute difference : {diff})"

    for sympy_fn, num_params in polys:
        args = params[:num_params] + (x,)
        f = lambdify(args, sympy_fn(*args))
        for _ in range(10):
            tn = numpy.random.randint(3, 10)
            tparams = tuple(numpy.random.uniform(0, 5, size=num_params-1))
            tv = numpy.random.uniform(-10, 10) + 1j*numpy.random.uniform(-5, 5)
            # SciPy supports hermite for real arguments only
            if sympy_fn == hermite:
                tv = numpy.real(tv)
            # assoc_legendre needs x in (-1, 1) and integer param at most n
            if sympy_fn == assoc_legendre:
                tv = numpy.random.uniform(-1, 1)
                tparams = tuple(numpy.random.randint(1, tn, size=1))

            vals = (tn,) + tparams + (tv,)
            scipy_result = f(*vals)
            sympy_result = sympy_fn(*vals).evalf()
            atol = 1e-9*(1 + abs(sympy_result))
            diff = abs(scipy_result - sympy_result)
            try:
                assert diff < atol
            except TypeError:
                raise AssertionError(
                    msg.format(
                        func=repr(sympy_fn),
                        args=repr(vals),
                        sympy_result=repr(sympy_result),
                        scipy_result=repr(scipy_result),
                        diff=diff,
                        tol=atol)
                    )

