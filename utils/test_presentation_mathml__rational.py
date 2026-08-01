
def test_presentation_mathml_Rational():
    mml_1 = mpp._print(Rational(1, 1))
    assert mml_1.nodeName == 'mn'

    mml_2 = mpp._print(Rational(2, 5))
    assert mml_2.nodeName == 'mfrac'
    assert mml_2.childNodes[0].childNodes[0].nodeValue == '2'
    assert mml_2.childNodes[1].childNodes[0].nodeValue == '5'

