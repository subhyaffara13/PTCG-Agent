
def test_print_polylog():
    assert mp.doprint(polylog(x, y)) == \
        '<apply><polylog/><ci>x</ci><ci>y</ci></apply>'
    assert mpp.doprint(polylog(x, y)) == \
        '<mrow><msub><mi>Li</mi><mi>x</mi></msub><mrow><mo>(</mo><mi>y</mi><mo>)</mo></mrow></mrow>'


def test_print_polylog():
    # Part of issue 6013
    uresult = 'Li₂(3)'
    aresult = 'polylog(2, 3)'
    assert pretty(polylog(2, 3)) == aresult
    assert upretty(polylog(2, 3)) == uresult

