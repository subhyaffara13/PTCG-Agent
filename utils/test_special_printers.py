
def test_special_printers():
    from sympy.printing.lambdarepr import IntervalPrinter

    def intervalrepr(expr):
        return IntervalPrinter().doprint(expr)

    expr = sqrt(sqrt(2) + sqrt(3)) + S.Half

    func0 = lambdify((), expr, modules="mpmath", printer=intervalrepr)
    func1 = lambdify((), expr, modules="mpmath", printer=IntervalPrinter)
    func2 = lambdify((), expr, modules="mpmath", printer=IntervalPrinter())

    mpi = type(mpmath.mpi(1, 2))

    assert isinstance(func0(), mpi)
    assert isinstance(func1(), mpi)
    assert isinstance(func2(), mpi)

    # To check Is lambdify loggamma works for mpmath or not
    exp1 = lambdify(x, loggamma(x), 'mpmath')(5)
    exp2 = lambdify(x, loggamma(x), 'mpmath')(1.8)
    exp3 = lambdify(x, loggamma(x), 'mpmath')(15)
    exp_ls = [exp1, exp2, exp3]

    sol1 = mpmath.loggamma(5)
    sol2 = mpmath.loggamma(1.8)
    sol3 = mpmath.loggamma(15)
    sol_ls = [sol1, sol2, sol3]

    assert exp_ls == sol_ls

