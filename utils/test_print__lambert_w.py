
def test_print_LambertW():
    assert mpp.doprint(LambertW(x)) == '<mrow><mi>W</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(LambertW(x, y)) == '<mrow><mi>W</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow></mrow>'

