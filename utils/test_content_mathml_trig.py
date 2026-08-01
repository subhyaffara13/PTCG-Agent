
def test_content_mathml_trig():
    mml = mp._print(sin(x))
    assert mml.childNodes[0].nodeName == 'sin'

    mml = mp._print(cos(x))
    assert mml.childNodes[0].nodeName == 'cos'

    mml = mp._print(tan(x))
    assert mml.childNodes[0].nodeName == 'tan'

    mml = mp._print(cot(x))
    assert mml.childNodes[0].nodeName == 'cot'

    mml = mp._print(csc(x))
    assert mml.childNodes[0].nodeName == 'csc'

    mml = mp._print(sec(x))
    assert mml.childNodes[0].nodeName == 'sec'

    mml = mp._print(asin(x))
    assert mml.childNodes[0].nodeName == 'arcsin'

    mml = mp._print(acos(x))
    assert mml.childNodes[0].nodeName == 'arccos'

    mml = mp._print(atan(x))
    assert mml.childNodes[0].nodeName == 'arctan'

    mml = mp._print(acot(x))
    assert mml.childNodes[0].nodeName == 'arccot'

    mml = mp._print(acsc(x))
    assert mml.childNodes[0].nodeName == 'arccsc'

    mml = mp._print(asec(x))
    assert mml.childNodes[0].nodeName == 'arcsec'

    mml = mp._print(sinh(x))
    assert mml.childNodes[0].nodeName == 'sinh'

    mml = mp._print(cosh(x))
    assert mml.childNodes[0].nodeName == 'cosh'

    mml = mp._print(tanh(x))
    assert mml.childNodes[0].nodeName == 'tanh'

    mml = mp._print(coth(x))
    assert mml.childNodes[0].nodeName == 'coth'

    mml = mp._print(csch(x))
    assert mml.childNodes[0].nodeName == 'csch'

    mml = mp._print(sech(x))
    assert mml.childNodes[0].nodeName == 'sech'

    mml = mp._print(asinh(x))
    assert mml.childNodes[0].nodeName == 'arcsinh'

    mml = mp._print(atanh(x))
    assert mml.childNodes[0].nodeName == 'arctanh'

    mml = mp._print(acosh(x))
    assert mml.childNodes[0].nodeName == 'arccosh'

    mml = mp._print(acoth(x))
    assert mml.childNodes[0].nodeName == 'arccoth'

    mml = mp._print(acsch(x))
    assert mml.childNodes[0].nodeName == 'arccsch'

    mml = mp._print(asech(x))
    assert mml.childNodes[0].nodeName == 'arcsech'

