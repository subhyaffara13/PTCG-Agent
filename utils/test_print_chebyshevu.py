
def test_print_chebyshevu():
    assert mathml(chebyshevu(n, x), printer = 'presentation') == \
        '<mrow><msub><mo>U</mo><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

