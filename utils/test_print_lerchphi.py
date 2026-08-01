
def test_print_lerchphi():
    assert mpp.doprint(lerchphi(1, 2, 3)) == \
        '<mrow><mi>&#x3A6;</mi><mrow><mo>(</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mn>3</mn><mo>)</mo></mrow></mrow>'


def test_print_lerchphi():
    # Part of issue 6013
    a = Symbol('a')
    pretty(lerchphi(a, 1, 2))
    uresult = 'Φ(a, 1, 2)'
    aresult = 'lerchphi(a, 1, 2)'
    assert pretty(lerchphi(a, 1, 2)) == aresult
    assert upretty(lerchphi(a, 1, 2)) == uresult

