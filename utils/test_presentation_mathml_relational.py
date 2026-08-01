
def test_presentation_mathml_relational():
    mml_1 = mpp._print(Eq(x, 1))
    assert len(mml_1.childNodes) == 3
    assert mml_1.childNodes[0].nodeName == 'mi'
    assert mml_1.childNodes[0].childNodes[0].nodeValue == 'x'
    assert mml_1.childNodes[1].nodeName == 'mo'
    assert mml_1.childNodes[1].childNodes[0].nodeValue == '='
    assert mml_1.childNodes[2].nodeName == 'mn'
    assert mml_1.childNodes[2].childNodes[0].nodeValue == '1'

    mml_2 = mpp._print(Ne(1, x))
    assert len(mml_2.childNodes) == 3
    assert mml_2.childNodes[0].nodeName == 'mn'
    assert mml_2.childNodes[0].childNodes[0].nodeValue == '1'
    assert mml_2.childNodes[1].nodeName == 'mo'
    assert mml_2.childNodes[1].childNodes[0].nodeValue == '&#x2260;'
    assert mml_2.childNodes[2].nodeName == 'mi'
    assert mml_2.childNodes[2].childNodes[0].nodeValue == 'x'

    mml_3 = mpp._print(Ge(1, x))
    assert len(mml_3.childNodes) == 3
    assert mml_3.childNodes[0].nodeName == 'mn'
    assert mml_3.childNodes[0].childNodes[0].nodeValue == '1'
    assert mml_3.childNodes[1].nodeName == 'mo'
    assert mml_3.childNodes[1].childNodes[0].nodeValue == '&#x2265;'
    assert mml_3.childNodes[2].nodeName == 'mi'
    assert mml_3.childNodes[2].childNodes[0].nodeValue == 'x'

    mml_4 = mpp._print(Lt(1, x))
    assert len(mml_4.childNodes) == 3
    assert mml_4.childNodes[0].nodeName == 'mn'
    assert mml_4.childNodes[0].childNodes[0].nodeValue == '1'
    assert mml_4.childNodes[1].nodeName == 'mo'
    assert mml_4.childNodes[1].childNodes[0].nodeValue == '<'
    assert mml_4.childNodes[2].nodeName == 'mi'
    assert mml_4.childNodes[2].childNodes[0].nodeValue == 'x'

