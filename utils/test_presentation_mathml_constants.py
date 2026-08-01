
def test_presentation_mathml_constants():
    mml = mpp._print(I)
    assert mml.childNodes[0].nodeValue == '&ImaginaryI;'

    mml = mpp._print(E)
    assert mml.childNodes[0].nodeValue == '&ExponentialE;'

    mml = mpp._print(oo)
    assert mml.childNodes[0].nodeValue == '&#x221E;'

    mml = mpp._print(pi)
    assert mml.childNodes[0].nodeValue == '&pi;'

    assert mathml(hbar, printer='presentation') == '<mi>&#x210F;</mi>'
    assert mathml(S.TribonacciConstant, printer='presentation'
        ) == '<mi>TribonacciConstant</mi>'
    assert mathml(S.EulerGamma, printer='presentation'
        ) == '<mi>&#x3B3;</mi>'
    assert mathml(S.GoldenRatio, printer='presentation'
        ) == '<mi>&#x3A6;</mi>'

    assert mathml(zoo, printer='presentation') == \
        '<mover><mo>&#x221E;</mo><mo>~</mo></mover>'

    assert mathml(S.NaN, printer='presentation') == '<mi>NaN</mi>'

