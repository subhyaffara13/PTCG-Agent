
def test_presentation_mathml_add():
    mml = mpp._print(x**5 - x**4 + x)
    assert len(mml.childNodes) == 5
    assert mml.childNodes[0].childNodes[0].childNodes[0
        ].nodeValue == 'x'
    assert mml.childNodes[0].childNodes[1].childNodes[0
        ].nodeValue == '5'
    assert mml.childNodes[1].childNodes[0].nodeValue == '-'
    assert mml.childNodes[2].childNodes[0].childNodes[0
        ].nodeValue == 'x'
    assert mml.childNodes[2].childNodes[1].childNodes[0
        ].nodeValue == '4'
    assert mml.childNodes[3].childNodes[0].nodeValue == '+'
    assert mml.childNodes[4].childNodes[0].nodeValue == 'x'

