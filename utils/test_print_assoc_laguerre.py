
def test_print_assoc_laguerre():
    assert mathml(assoc_laguerre(n, a, x), printer = 'presentation') == \
        '<mrow><msubsup><mo>L</mo><mi>n</mi><mrow><mo>(</mo><mi>a</mi><mo>)</mo></mrow></msubsup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

