
def test_print_chebyshevt():
    assert mathml(chebyshevt(n, x), printer = 'presentation') == \
        '<mrow><msub><mo>T</mo><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

