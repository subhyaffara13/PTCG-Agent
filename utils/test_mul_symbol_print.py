
def test_mul_symbol_print():
    expr = x * y
    assert mathml(expr, printer='presentation') == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mi>y</mi></mrow>'
    assert mathml(expr, printer='presentation', mul_symbol=None) == \
        '<mrow><mi>x</mi><mo>&InvisibleTimes;</mo><mi>y</mi></mrow>'
    assert mathml(expr, printer='presentation', mul_symbol='dot') == \
        '<mrow><mi>x</mi><mo>&#xB7;</mo><mi>y</mi></mrow>'
    assert mathml(expr, printer='presentation', mul_symbol='ldot') == \
        '<mrow><mi>x</mi><mo>&#x2024;</mo><mi>y</mi></mrow>'
    assert mathml(expr, printer='presentation', mul_symbol='times') == \
        '<mrow><mi>x</mi><mo>&#xD7;</mo><mi>y</mi></mrow>'

