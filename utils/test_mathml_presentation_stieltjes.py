
def test_mathml_presentation_stieltjes():
    assert mathml(stieltjes(n), printer='presentation') == \
         '<msub><mi>&#x03B3;</mi><mi>n</mi></msub>'
    assert mathml(stieltjes(n, x), printer='presentation') == \
         '<mrow><msub><mi>&#x03B3;</mi><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

