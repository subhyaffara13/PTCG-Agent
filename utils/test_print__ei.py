
def test_print_Ei():
    assert mathml(Ei(x), printer = 'presentation') == \
        '<mrow><mi>Ei</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(Ei(x**y), printer = 'presentation') == \
        '<mrow><mi>Ei</mi><mrow><mo>(</mo><msup><mi>x</mi><mi>y</mi></msup><mo>)</mo></mrow></mrow>'

