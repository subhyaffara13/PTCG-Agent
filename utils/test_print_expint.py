
def test_print_expint():
    assert mathml(expint(x, y), printer = 'presentation') == \
        '<mrow><msub><mo>E</mo><mi>x</mi></msub><mrow><mo>(</mo><mi>y</mi><mo>)</mo></mrow></mrow>'
    assert mathml(expint(IndexedBase(x)[1], IndexedBase(x)[2]), printer = 'presentation') == \
        '<mrow><msub><mo>E</mo><msub><mi>x</mi><mn>1</mn></msub></msub><mrow><mo>(</mo><msub><mi>x</mi><mn>2</mn></msub><mo>)</mo></mrow></mrow>'

