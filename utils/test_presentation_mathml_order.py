
def test_presentation_mathml_order():
    expr = x**3 + x**2*y + 3*x*y**3 + y**4

    mp = MathMLPresentationPrinter({'order': 'lex'})
    mml = mp._print(expr)
    assert mml.childNodes[0].nodeName == 'msup'
    assert mml.childNodes[0].childNodes[0].childNodes[0].nodeValue == 'x'
    assert mml.childNodes[0].childNodes[1].childNodes[0].nodeValue == '3'

    assert mml.childNodes[6].nodeName == 'msup'
    assert mml.childNodes[6].childNodes[0].childNodes[0].nodeValue == 'y'
    assert mml.childNodes[6].childNodes[1].childNodes[0].nodeValue == '4'

    mp = MathMLPresentationPrinter({'order': 'rev-lex'})
    mml = mp._print(expr)

    assert mml.childNodes[0].nodeName == 'msup'
    assert mml.childNodes[0].childNodes[0].childNodes[0].nodeValue == 'y'
    assert mml.childNodes[0].childNodes[1].childNodes[0].nodeValue == '4'

    assert mml.childNodes[6].nodeName == 'msup'
    assert mml.childNodes[6].childNodes[0].childNodes[0].nodeValue == 'x'
    assert mml.childNodes[6].childNodes[1].childNodes[0].nodeValue == '3'

