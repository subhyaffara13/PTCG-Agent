
def test_print_intervals():
    a = Symbol('a', real=True)
    assert mpp.doprint(Interval(0, a)) == \
        '<mrow><mo>[</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>]</mo></mrow>'
    assert mpp.doprint(Interval(0, a, False, False)) == \
        '<mrow><mo>[</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>]</mo></mrow>'
    assert mpp.doprint(Interval(0, a, True, False)) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>]</mo></mrow>'
    assert mpp.doprint(Interval(0, a, False, True)) == \
        '<mrow><mo>[</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>)</mo></mrow>'
    assert mpp.doprint(Interval(0, a, True, True)) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>)</mo></mrow>'

