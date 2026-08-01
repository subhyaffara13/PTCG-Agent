
def test_print_elliptic_pi():
    assert mathml(elliptic_pi(x, y), printer = 'presentation') == \
        '<mrow><mi>&#x1d6f1;</mi><mrow><mo>(</mo><mi>x</mi><mo>|</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mathml(elliptic_pi(x, y, z), printer = 'presentation') == \
        '<mrow><mi>&#x1d6f1;</mi><mrow><mo>(</mo><mi>x</mi><mo>;</mo><mi>y</mi><mo>|</mo><mi>z</mi><mo>)</mo></mrow></mrow>'

