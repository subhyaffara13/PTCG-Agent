
def test_mathml_Range():
    assert mpp.doprint(Range(1, 51)) == \
        '<mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mi>&#8230;</mi><mo>,</mo><mn>50</mn><mo>}</mo></mrow>'
    assert mpp.doprint(Range(1, 4)) == \
        '<mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mn>3</mn><mo>}</mo></mrow>'
    assert mpp.doprint(Range(0, 3, 1)) == \
        '<mrow><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>}</mo></mrow>'
    assert mpp.doprint(Range(0, 30, 1)) == \
        '<mrow><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>,</mo><mi>&#8230;</mi><mo>,</mo><mn>29</mn><mo>}</mo></mrow>'
    assert mpp.doprint(Range(30, 1, -1)) == \
        '<mrow><mo>{</mo><mn>30</mn><mo>,</mo><mn>29</mn><mo>,</mo><mi>&#8230;</mi><mo>,</mo><mn>2</mn><mo>}</mo></mrow>'
    assert mpp.doprint(Range(0, oo, 2)) == \
        '<mrow><mo>{</mo><mn>0</mn><mo>,</mo><mn>2</mn><mo>,</mo><mi>&#8230;</mi><mo>}</mo></mrow>'
    assert mpp.doprint(Range(oo, -2, -2)) == \
        '<mrow><mo>{</mo><mi>&#8230;</mi><mo>,</mo><mn>2</mn><mo>,</mo><mn>0</mn><mo>}</mo></mrow>'
    assert mpp.doprint(Range(-2, -oo, -1)) == \
        '<mrow><mo>{</mo><mn>-2</mn><mo>,</mo><mn>-3</mn><mo>,</mo><mi>&#8230;</mi><mo>}</mo></mrow>'

