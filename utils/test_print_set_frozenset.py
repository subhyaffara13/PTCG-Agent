
def test_print_set_frozenset():
    f = frozenset({1, 5, 3})
    assert mpp.doprint(f) == \
        '<mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>3</mn><mo>,</mo><mn>5</mn><mo>}</mo></mrow>'
    s = set({1, 2, 3})
    assert mpp.doprint(s) == \
        '<mrow><mo>{</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mn>3</mn><mo>}</mo></mrow>'

