
def test_print_exp():
    assert mpp.doprint(exp(x)) == \
        '<msup><mi>&ExponentialE;</mi><mi>x</mi></msup>'
    assert mpp.doprint(exp(1) + exp(2)) == \
        '<mrow><mi>&ExponentialE;</mi><mo>+</mo><msup><mi>&ExponentialE;</mi><mn>2</mn></msup></mrow>'

