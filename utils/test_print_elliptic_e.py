
def test_print_elliptic_e():
    assert mathml(elliptic_e(x), printer = 'presentation') == \
        '<mrow><mi>&#x1d5a4;</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(elliptic_e(x, y), printer = 'presentation') == \
        '<mrow><mi>&#x1d5a4;</mi><mrow><mo>(</mo><mi>x</mi><mo>|</mo><mi>y</mi><mo>)</mo></mrow></mrow>'

