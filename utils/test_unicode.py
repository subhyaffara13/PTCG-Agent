
def test_unicode():
    xu = Symbol('x')
    x = Symbol('x')
    assert x == xu

    raises(TypeError, lambda: Symbol(1))


def test_unicode():
    mp.dps = 15
    try:
        unicode = unicode
    except NameError:
        unicode = str
    assert mpf(unicode('2.76')) == 2.76
    assert mpf(unicode('inf')) == inf

