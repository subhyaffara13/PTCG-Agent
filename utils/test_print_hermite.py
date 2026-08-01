
def test_print_hermite():
    assert mathml(hermite(n, x), printer = 'presentation') == \
        '<mrow><msub><mo>H</mo><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

