
def test_print_Abs():
    assert mpp.doprint(Abs(x)) == \
        '<mrow><mo>|</mo><mi>x</mi><mo>|</mo></mrow>'
    assert mpp.doprint(Abs(x + 1)) == \
        '<mrow><mo>|</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>|</mo></mrow>'

