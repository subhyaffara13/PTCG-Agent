
def test_print_legendre():
    assert mathml(legendre(n, x), printer = 'presentation') == \
        '<mrow><msub><mo>P</mo><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

