
def test_numbered_symbols():
    s = numbered_symbols(cls=Dummy)
    assert isinstance(next(s), Dummy)
    assert next(numbered_symbols('C', start=1, exclude=[symbols('C1')])) == \
        symbols('C2')


def test_numbered_symbols():
    ns = cse_main.numbered_symbols(prefix='y')
    assert list(itertools.islice(
        ns, 0, 10)) == [Symbol('y%s' % i) for i in range(0, 10)]
    ns = cse_main.numbered_symbols(prefix='y')
    assert list(itertools.islice(
        ns, 10, 20)) == [Symbol('y%s' % i) for i in range(10, 20)]
    ns = cse_main.numbered_symbols()
    assert list(itertools.islice(
        ns, 0, 10)) == [Symbol('x%s' % i) for i in range(0, 10)]

