
def test_print_AccumBounds():
    a = Symbol('a', real=True)
    assert mpp.doprint(AccumBounds(0, 1)) == '<mrow><mo>&#10216;</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>&#10217;</mo></mrow>'
    assert mpp.doprint(AccumBounds(0, a)) == '<mrow><mo>&#10216;</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>&#10217;</mo></mrow>'
    assert mpp.doprint(AccumBounds(a + 1, a + 2)) == '<mrow><mo>&#10216;</mo><mrow><mi>a</mi><mo>+</mo><mn>1</mn></mrow><mo>,</mo><mrow><mi>a</mi><mo>+</mo><mn>2</mn></mrow><mo>&#10217;</mo></mrow>'

