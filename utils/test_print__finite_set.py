
def test_print_FiniteSet():
    f1 = FiniteSet(x, 1, 3)
    assert mpp.doprint(f1) == \
        '<mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>3</mn><mo>,</mo><mi>x</mi><mo>}</mo></mrow>'

