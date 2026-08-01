
def test_presentation_mathml_functions():
    mml_1 = mpp._print(sin(x))
    assert mml_1.childNodes[0].childNodes[0
        ].nodeValue == 'sin'
    assert mml_1.childNodes[1].childNodes[1
        ].childNodes[0].nodeValue == 'x'

    mml_2 = mpp._print(diff(sin(x), x, evaluate=False))
    assert mml_2.nodeName == 'mrow'
    assert mml_2.childNodes[0].childNodes[0
        ].childNodes[0].childNodes[0].nodeValue == '&dd;'
    assert mml_2.childNodes[1].childNodes[1
        ].nodeName == 'mrow'
    assert mml_2.childNodes[0].childNodes[1
        ].childNodes[0].childNodes[0].nodeValue == '&dd;'

    mml_3 = mpp._print(diff(cos(x*y), x, evaluate=False))
    assert mml_3.childNodes[0].nodeName == 'mfrac'
    assert mml_3.childNodes[0].childNodes[0
        ].childNodes[0].childNodes[0].nodeValue == '&#x2202;'
    assert mml_3.childNodes[1].childNodes[0
        ].childNodes[0].nodeValue == 'cos'

