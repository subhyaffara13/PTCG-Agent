
def test_print_re_im():
    assert mpp.doprint(re(x)) == \
        '<mrow><mi>&#8476;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(im(x)) == \
        '<mrow><mi>&#8465;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(re(x + 1, evaluate=False)) == \
        '<mrow><mi>&#8476;</mi><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(im(x + 1, evaluate=False)) == \
        '<mrow><mi>&#8465;</mi><mrow><mo>(</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow>'

