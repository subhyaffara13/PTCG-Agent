
def test_presentation_mathml_limits():
    lim_fun = sin(x)/x
    mml_1 = mpp._print(Limit(lim_fun, x, 0))
    assert mml_1.childNodes[0].nodeName == 'munder'
    assert mml_1.childNodes[0].childNodes[0
        ].childNodes[0].nodeValue == 'lim'
    assert mml_1.childNodes[0].childNodes[1
        ].childNodes[0].childNodes[0
        ].nodeValue == 'x'
    assert mml_1.childNodes[0].childNodes[1
        ].childNodes[1].childNodes[0
        ].nodeValue == '&#x2192;'
    assert mml_1.childNodes[0].childNodes[1
        ].childNodes[2].childNodes[0
        ].nodeValue == '0'

