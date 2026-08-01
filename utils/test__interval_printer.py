
def test_IntervalPrinter():
    ip = IntervalPrinter()
    assert ip.doprint(x**Rational(1, 3)) == "x**(mpi('1/3'))"
    assert ip.doprint(sqrt(x)) == "x**(mpi('1/2'))"

