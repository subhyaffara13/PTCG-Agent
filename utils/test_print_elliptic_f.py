
def test_print_elliptic_f():
    assert mathml(elliptic_f(x, y), printer = 'presentation') == \
        '<mrow><mi>&#x1d5a5;</mi><mrow><mo>(</mo><mi>x</mi><mo>|</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mathml(elliptic_f(x/y, y), printer = 'presentation') == \
        '<mrow><mi>&#x1d5a5;</mi><mrow><mo>(</mo><mrow><mfrac><mi>x</mi><mi>y</mi></mfrac></mrow><mo>|</mo><mi>y</mi><mo>)</mo></mrow></mrow>'

