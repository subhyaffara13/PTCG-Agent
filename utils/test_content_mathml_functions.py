
def test_content_mathml_functions():
    mml_1 = mp._print(sin(x))
    assert mml_1.nodeName == 'apply'
    assert mml_1.childNodes[0].nodeName == 'sin'
    assert mml_1.childNodes[1].nodeName == 'ci'

    mml_2 = mp._print(diff(sin(x), x, evaluate=False))
    assert mml_2.nodeName == 'apply'
    assert mml_2.childNodes[0].nodeName == 'diff'
    assert mml_2.childNodes[1].nodeName == 'bvar'
    assert mml_2.childNodes[1].childNodes[
        0].nodeName == 'ci'  # below bvar there's <ci>x/ci>

    mml_3 = mp._print(diff(cos(x*y), x, evaluate=False))
    assert mml_3.nodeName == 'apply'
    assert mml_3.childNodes[0].nodeName == 'partialdiff'
    assert mml_3.childNodes[1].nodeName == 'bvar'
    assert mml_3.childNodes[1].childNodes[
        0].nodeName == 'ci'  # below bvar there's <ci>x/ci>

    mml_4 = mp._print(Lambda((x, y), x * y))
    assert mml_4.nodeName == 'lambda'
    assert mml_4.childNodes[0].nodeName == 'bvar'
    assert mml_4.childNodes[0].childNodes[
        0].nodeName == 'ci'  # below bvar there's <ci>x/ci>
    assert mml_4.childNodes[1].nodeName == 'bvar'
    assert mml_4.childNodes[1].childNodes[
        0].nodeName == 'ci'  # below bvar there's <ci>y/ci>
    assert mml_4.childNodes[2].nodeName == 'apply'

