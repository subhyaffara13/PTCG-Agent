
def test_content_mathml_Rational():
    mml_1 = mp._print(Rational(1, 1))
    """should just return a number"""
    assert mml_1.nodeName == 'cn'

    mml_2 = mp._print(Rational(2, 5))
    assert mml_2.childNodes[0].nodeName == 'divide'

