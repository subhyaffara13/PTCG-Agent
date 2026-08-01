
def test_issue_17857():
    assert mathml(Range(-oo, oo), printer='presentation') == \
        '<mrow><mo>{</mo><mi>&#8230;</mi><mo>,</mo><mn>-1</mn><mo>,</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>,</mo><mi>&#8230;</mi><mo>}</mo></mrow>'
    assert mathml(Range(oo, -oo, -1), printer='presentation') == \
        '<mrow><mo>{</mo><mi>&#8230;</mi><mo>,</mo><mn>1</mn><mo>,</mo><mn>0</mn><mo>,</mo><mn>-1</mn><mo>,</mo><mi>&#8230;</mi><mo>}</mo></mrow>'


def test_issue_17857():
    assert pretty(Range(-oo, oo)) == '{..., -1, 0, 1, ...}'
    assert pretty(Range(oo, -oo, -1)) == '{..., 1, 0, -1, ...}'

