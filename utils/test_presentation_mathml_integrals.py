
def test_presentation_mathml_integrals():
    assert mpp.doprint(Integral(x, (x, 0, 1))) == \
        '<mrow><msubsup><mo>&#x222B;</mo><mn>0</mn><mn>1</mn></msubsup>'\
        '<mi>x</mi><mo>&dd;</mo><mi>x</mi></mrow>'
    assert mpp.doprint(Integral(log(x), x)) == \
        '<mrow><mo>&#x222B;</mo><mrow><mi>log</mi><mrow><mo>(</mo><mi>x</mi>' \
        '<mo>)</mo></mrow></mrow><mo>&dd;</mo><mi>x</mi></mrow>'
    assert mpp.doprint(Integral(x*y, x, y)) == \
        '<mrow><mo>&#x222C;</mo><mrow><mi>x</mi><mo>&InvisibleTimes;</mo>'\
        '<mi>y</mi></mrow><mo>&dd;</mo><mi>y</mi><mo>&dd;</mo><mi>x</mi></mrow>'
    z, w = symbols('z w')
    assert mpp.doprint(Integral(x*y*z, x, y, z)) == \
        '<mrow><mo>&#x222D;</mo><mrow><mi>x</mi><mo>&InvisibleTimes;</mo>'\
        '<mi>y</mi><mo>&InvisibleTimes;</mo><mi>z</mi></mrow><mo>&dd;</mo>'\
        '<mi>z</mi><mo>&dd;</mo><mi>y</mi><mo>&dd;</mo><mi>x</mi></mrow>'
    assert mpp.doprint(Integral(x*y*z*w, x, y, z, w)) == \
        '<mrow><mo>&#x222B;</mo><mo>&#x222B;</mo><mo>&#x222B;</mo>'\
        '<mo>&#x222B;</mo><mrow><mi>w</mi><mo>&InvisibleTimes;</mo>'\
        '<mi>x</mi><mo>&InvisibleTimes;</mo><mi>y</mi>'\
        '<mo>&InvisibleTimes;</mo><mi>z</mi></mrow><mo>&dd;</mo><mi>w</mi>'\
        '<mo>&dd;</mo><mi>z</mi><mo>&dd;</mo><mi>y</mi><mo>&dd;</mo><mi>x</mi></mrow>'
    assert mpp.doprint(Integral(x, x, y, (z, 0, 1))) == \
        '<mrow><msubsup><mo>&#x222B;</mo><mn>0</mn><mn>1</mn></msubsup>'\
        '<mo>&#x222B;</mo><mo>&#x222B;</mo><mi>x</mi><mo>&dd;</mo><mi>z</mi>'\
        '<mo>&dd;</mo><mi>y</mi><mo>&dd;</mo><mi>x</mi></mrow>'
    assert mpp.doprint(Integral(x, (x, 0))) == \
        '<mrow><msup><mo>&#x222B;</mo><mn>0</mn></msup><mi>x</mi><mo>&dd;</mo>'\
        '<mi>x</mi></mrow>'

