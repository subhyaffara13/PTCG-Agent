
def test_print_expression_with_minus():
    assert mpp.doprint(-x) == '<mrow><mo>-</mo><mi>x</mi></mrow>'
    assert mpp.doprint(-x/y) == \
        '<mrow><mo>-</mo><mfrac><mi>x</mi><mi>y</mi></mfrac></mrow>'
    assert mpp.doprint(-Rational(1, 2)) == \
        '<mrow><mo>-</mo><mfrac><mn>1</mn><mn>2</mn></mfrac></mrow>'

