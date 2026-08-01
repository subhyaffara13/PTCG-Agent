
def test_print_MinMax():
    assert mpp.doprint(Min(x, y)) == \
        '<mrow><mo>min</mo><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(Min(x, 2, x**3)) == \
        '<mrow><mo>min</mo><mrow><mo>(</mo><mn>2</mn><mo>,</mo><mi>x</mi><mo>,</mo><msup><mi>x</mi><mn>3</mn></msup><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(Max(x, y)) == \
        '<mrow><mo>max</mo><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mpp.doprint(Max(x, 2, x**3)) == \
        '<mrow><mo>max</mo><mrow><mo>(</mo><mn>2</mn><mo>,</mo><mi>x</mi><mo>,</mo><msup><mi>x</mi><mn>3</mn></msup><mo>)</mo></mrow></mrow>'

