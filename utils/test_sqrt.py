
def test_sqrt():
    f = lambdify(x, sqrt(x))
    assert f(0) == 0.0
    assert f(1) == 1.0
    assert f(4) == 2.0
    assert abs(f(2) - 1.414) < 0.001
    assert f(6.25) == 2.5


def test_sqrt():
    prntr = LambdaPrinter({'standard' : 'python3'})
    assert prntr._print_Pow(sqrt(x), rational=False) == 'sqrt(x)'
    assert prntr._print_Pow(sqrt(x), rational=True) == 'x**(1/2)'


def test_sqrt():
    if not np:
        skip("NumPy not installed")
    assert abs(lambdify((a,), sqrt(a), 'numpy')(4) - 2) <= NUMPY_DEFAULT_EPSILON


def test_sqrt():
    prntr = PythonCodePrinter()
    assert prntr._print_Pow(sqrt(x), rational=False) == 'math.sqrt(x)'
    assert prntr._print_Pow(1/sqrt(x), rational=False) == '1/math.sqrt(x)'

    prntr = PythonCodePrinter({'standard' : 'python3'})
    assert prntr._print_Pow(sqrt(x), rational=True) == 'x**(1/2)'
    assert prntr._print_Pow(1/sqrt(x), rational=True) == 'x**(-1/2)'

    prntr = MpmathPrinter()
    assert prntr._print_Pow(sqrt(x), rational=False) == 'mpmath.sqrt(x)'
    assert prntr._print_Pow(sqrt(x), rational=True) == \
        "x**(mpmath.mpf(1)/mpmath.mpf(2))"

    prntr = NumPyPrinter()
    assert prntr._print_Pow(sqrt(x), rational=False) == 'numpy.sqrt(x)'
    assert prntr._print_Pow(sqrt(x), rational=True) == 'x**(1/2)'

    prntr = SciPyPrinter()
    assert prntr._print_Pow(sqrt(x), rational=False) == 'numpy.sqrt(x)'
    assert prntr._print_Pow(sqrt(x), rational=True) == 'x**(1/2)'

    prntr = SymPyPrinter()
    assert prntr._print_Pow(sqrt(x), rational=False) == 'sympy.sqrt(x)'
    assert prntr._print_Pow(sqrt(x), rational=True) == 'x**(1/2)'


def test_sqrt():
    assert str(sqrt(x)) == "sqrt(x)"
    assert str(sqrt(x**2)) == "sqrt(x**2)"
    assert str(1/sqrt(x)) == "1/sqrt(x)"
    assert str(1/sqrt(x**2)) == "1/sqrt(x**2)"
    assert str(y/sqrt(x)) == "y/sqrt(x)"
    assert str(x**0.5) == "x**0.5"
    assert str(1/x**0.5) == "x**(-0.5)"


def test_sqrt():
    a = sqrt(interval(1, 4))
    assert a.start == 1
    assert a.end == 2

    a = sqrt(interval(0.01, 1))
    assert a.start == np.sqrt(0.01)
    assert a.end == 1

    a = sqrt(interval(-1, 1))
    assert a.is_valid is None

    a = sqrt(interval(-3, -1))
    assert a.is_valid is False

    a = sqrt(4)
    assert (a == interval(2, 2)) == (True, True)

    a = sqrt(-3)
    assert a.is_valid is False


def test_sqrt():
    # this fails quite often. it appers to be float
    # that rounds the wrong way, not mpf
    fail = 0
    mp.prec = 53
    for x in xs:
        x = abs(x)
        mp.prec = 100
        mp_high = mpf(x)**0.5
        mp.prec = 53
        mp_low = mpf(x)**0.5
        fp = x**0.5
        assert abs(mp_low-mp_high) <= abs(fp-mp_high)
        fail += mp_low != fp
    assert fail < N/10

