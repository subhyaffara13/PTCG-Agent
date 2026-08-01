
def test_print_gegenbauer():
    assert mathml(gegenbauer(n, a, x), printer = 'presentation') == \
        '<mrow><msubsup><mo>C</mo><mi>n</mi><mrow><mo>(</mo><mi>a</mi><mo>)</mo></mrow></msubsup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

