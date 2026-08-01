
def test_print_Lambda():
    expr = Lambda(x, x+1)
    assert mathml(expr, printer='presentation') == \
        '<mrow><mo>(</mo><mi>x</mi><mo>&#x21A6;</mo><mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow>'
    expr = Lambda((x, y), x + y)
    assert mathml(expr, printer='presentation') == \
        '<mrow><mo>(</mo><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></mrow><mo>&#x21A6;</mo><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow><mo>)</mo></mrow>'

