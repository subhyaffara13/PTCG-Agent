
def test_presentation_mathml_trig():
    mml = mpp._print(sin(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'sin'

    mml = mpp._print(cos(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'cos'

    mml = mpp._print(tan(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'tan'

    mml = mpp._print(asin(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'arcsin'

    mml = mpp._print(acos(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'arccos'

    mml = mpp._print(atan(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'arctan'

    mml = mpp._print(sinh(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'sinh'

    mml = mpp._print(cosh(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'cosh'

    mml = mpp._print(tanh(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'tanh'

    mml = mpp._print(asinh(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'arcsinh'

    mml = mpp._print(atanh(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'arctanh'

    mml = mpp._print(acosh(x))
    assert mml.childNodes[0].childNodes[0].nodeValue == 'arccosh'

