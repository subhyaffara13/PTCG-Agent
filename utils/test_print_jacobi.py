
def test_print_jacobi():
    assert mathml(jacobi(n, a, b, x), printer = 'presentation') == \
        '<mrow><msubsup><mo>P</mo><mi>n</mi><mrow><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>)</mo></mrow></msubsup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

