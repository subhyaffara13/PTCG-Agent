
def test_print_derivative():
    f = Function('f')
    d = Derivative(f(x, y, z), x, z, x, z, z, y)
    assert mathml(d) == \
        '<apply><partialdiff/><bvar><ci>y</ci><ci>z</ci><degree><cn>2</cn></degree><ci>x</ci><ci>z</ci><ci>x</ci></bvar><apply><f/><ci>x</ci><ci>y</ci><ci>z</ci></apply></apply>'
    assert mathml(d, printer='presentation') == \
        '<mrow><mfrac><mrow><msup><mo>&#x2202;</mo><mn>6</mn></msup></mrow><mrow><mo>&#x2202;</mo><mi>y</mi><msup><mo>&#x2202;</mo><mn>2</mn></msup><mi>z</mi><mo>&#x2202;</mo><mi>x</mi><mo>&#x2202;</mo><mi>z</mi><mo>&#x2202;</mo><mi>x</mi></mrow></mfrac><mrow><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>,</mo><mi>z</mi><mo>)</mo></mrow></mrow></mrow>'

