
def test_presentation_printmethod():
    assert mpp.doprint(1 + x) == '<mrow><mi>x</mi><mo>+</mo><mn>1</mn></mrow>'
    assert mpp.doprint(x**2) == '<msup><mi>x</mi><mn>2</mn></msup>'
    assert mpp.doprint(x**-1) == '<mfrac><mn>1</mn><mi>x</mi></mfrac>'
    assert mpp.doprint(x**-2) == \
        '<mfrac><mn>1</mn><msup><mi>x</mi><mn>2</mn></msup></mfrac>'
    assert mpp.doprint(2*x) == \
        '<mrow><mn>2</mn><mo>&InvisibleTimes;</mo><mi>x</mi></mrow>'

