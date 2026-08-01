
def test_mathml_presentation_mathieu():
    assert mathml(mathieuc(x, y, z), printer='presentation') == \
        '<mrow><mi>C</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>,</mo><mi>z</mi><mo>)</mo></mrow></mrow>'
    assert mathml(mathieus(x, y, z), printer='presentation') == \
        '<mrow><mi>S</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>,</mo><mi>z</mi><mo>)</mo></mrow></mrow>'
    assert mathml(mathieucprime(x, y, z), printer='presentation') == \
        '<mrow><mi>C&#x2032;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>,</mo><mi>z</mi><mo>)</mo></mrow></mrow>'
    assert mathml(mathieusprime(x, y, z), printer='presentation') == \
        '<mrow><mi>S&#x2032;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>,</mo><mi>z</mi><mo>)</mo></mrow></mrow>'

