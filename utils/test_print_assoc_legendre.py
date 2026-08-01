
def test_print_assoc_legendre():
    assert mathml(assoc_legendre(n, a, x), printer = 'presentation') == \
        '<mrow><msubsup><mo>P</mo><mi>n</mi><mrow><mo>(</mo><mi>a</mi><mo>)</mo></mrow></msubsup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

