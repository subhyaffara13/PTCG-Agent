
def test_print_different_functions():
    assert mpp.doprint(gamma(x)) == '<mrow><mi>&#x393;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(lowergamma(x, y)) == '<mrow><mi>&#x3B3;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(uppergamma(x, y)) == '<mrow><mi>&#x393;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(zeta(x)) == '<mrow><mi>&#x3B6;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(zeta(x, y)) == '<mrow><mi>&#x3B6;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(dirichlet_eta(x)) ==  '<mrow><mi>&#x3B7;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(elliptic_k(x)) == '<mrow><mi>&#x39A;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(totient(x)) == '<mrow><mi>&#x3D5;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(reduced_totient(x)) == '<mrow><mi>&#x3BB;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(primenu(x)) == '<mrow><mi>&#x3BD;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(primeomega(x)) == '<mrow><mi>&#x3A9;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(fresnels(x)) == '<mrow><mi>S</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(fresnelc(x)) ==  '<mrow><mi>C</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(Heaviside(x)) == '<mrow><mi>&#x398;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>)</mo></mrow></mrow>'

