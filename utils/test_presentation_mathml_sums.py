
def test_presentation_mathml_sums():
    mml_1 = mpp._print(Sum(x, (x, 1, 10)))
    assert mml_1.childNodes[0].nodeName == 'munderover'
    assert len(mml_1.childNodes[0].childNodes) == 3
    assert mml_1.childNodes[0].childNodes[0].childNodes[0
        ].nodeValue == '&#x2211;'
    assert len(mml_1.childNodes[0].childNodes[1].childNodes) == 3
    assert mml_1.childNodes[0].childNodes[2].childNodes[0
        ].nodeValue == '10'
    assert mml_1.childNodes[1].childNodes[0].nodeValue == 'x'

    assert mpp.doprint(Sum(x, (x, 1, 10))) == \
        '<mrow><munderover><mo>&#x2211;</mo><mrow><mi>x</mi><mo>=</mo><mn>1</mn></mrow><mn>10</mn></munderover><mi>x</mi></mrow>'
    assert mpp.doprint(Sum(x + y, (x, 1, 10))) == \
        '<mrow><munderover><mo>&#x2211;</mo><mrow><mi>x</mi><mo>=</mo><mn>1</mn></mrow><mn>10</mn></munderover><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow><mo>)</mo></mrow></mrow>'

