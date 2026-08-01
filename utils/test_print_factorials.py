
def test_print_factorials():
    assert mpp.doprint(factorial(x)) == '<mrow><mi>x</mi><mo>!</mo></mrow>'
    assert mpp.doprint(factorial(x + 1)) == \
        '<mrow><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow><mo>!</mo></mrow>'
    assert mpp.doprint(factorial2(x)) == '<mrow><mi>x</mi><mo>!!</mo></mrow>'
    assert mpp.doprint(factorial2(x + 1)) == \
        '<mrow><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow><mo>!!</mo></mrow>'
    assert mpp.doprint(binomial(x, y)) == \
        '<mrow><mo>(</mo><mfrac linethickness="0"><mi>x</mi><mi>y</mi></mfrac><mo>)</mo></mrow>'
    assert mpp.doprint(binomial(4, x + y)) == \
        '<mrow><mo>(</mo><mfrac linethickness="0"><mn>4</mn><mrow><mi>x</mi>'\
        '<mo>+</mo><mi>y</mi></mrow></mfrac><mo>)</mo></mrow>'

