
def test_print_laguerre():
    assert mathml(laguerre(n, x), printer = 'presentation') == \
        '<mrow><msub><mo>L</mo><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

