
def test_ln_notation_print():
    expr = log(x)
    assert mathml(expr, printer='presentation') == \
        '<mrow><mi>log</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(expr, printer='presentation', ln_notation=False) == \
        '<mrow><mi>log</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(expr, printer='presentation', ln_notation=True) == \
        '<mrow><mi>ln</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

