
def test_print_tuples():
    assert mpp.doprint(Tuple(0,)) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>)</mo></mrow>'
    assert mpp.doprint(Tuple(0, a)) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>)</mo></mrow>'
    assert mpp.doprint(Tuple(0, a, a)) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>,</mo><mi>a</mi><mo>)</mo></mrow>'
    assert mpp.doprint(Tuple(0, 1, 2, 3, 4)) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mn>3</mn><mo>,</mo><mn>4</mn><mo>)</mo></mrow>'
    assert mpp.doprint(Tuple(0, 1, Tuple(2, 3, 4))) == \
        '<mrow><mo>(</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>,</mo><mrow><mo>(</mo><mn>2</mn><mo>,</mo><mn>3'\
        '</mn><mo>,</mo><mn>4</mn><mo>)</mo></mrow><mo>)</mo></mrow>'

