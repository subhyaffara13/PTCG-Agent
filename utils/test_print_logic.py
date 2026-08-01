
def test_print_logic():
    assert mpp.doprint(And(x, y)) == \
        '<mrow><mi>x</mi><mo>&#x2227;</mo><mi>y</mi></mrow>'
    assert mpp.doprint(Or(x, y)) == \
        '<mrow><mi>x</mi><mo>&#x2228;</mo><mi>y</mi></mrow>'
    assert mpp.doprint(Xor(x, y)) == \
        '<mrow><mi>x</mi><mo>&#x22BB;</mo><mi>y</mi></mrow>'
    assert mpp.doprint(Implies(x, y)) == \
        '<mrow><mi>x</mi><mo>&#x21D2;</mo><mi>y</mi></mrow>'
    assert mpp.doprint(Equivalent(x, y)) == \
        '<mrow><mi>x</mi><mo>&#x21D4;</mo><mi>y</mi></mrow>'

    assert mpp.doprint(And(Eq(x, y), x > 4)) == \
        '<mrow><mrow><mi>x</mi><mo>=</mo><mi>y</mi></mrow><mo>&#x2227;</mo>'\
        '<mrow><mi>x</mi><mo>></mo><mn>4</mn></mrow></mrow>'
    assert mpp.doprint(And(Eq(x, 3), y < 3, x > y + 1)) == \
        '<mrow><mrow><mi>x</mi><mo>=</mo><mn>3</mn></mrow><mo>&#x2227;</mo>'\
        '<mrow><mi>x</mi><mo>></mo><mrow><mi>y</mi><mo>+</mo><mn>1</mn></mrow>'\
        '</mrow><mo>&#x2227;</mo><mrow><mi>y</mi><mo><</mo><mn>3</mn></mrow></mrow>'
    assert mpp.doprint(Or(Eq(x, y), x > 4)) == \
        '<mrow><mrow><mi>x</mi><mo>=</mo><mi>y</mi></mrow><mo>&#x2228;</mo>'\
        '<mrow><mi>x</mi><mo>></mo><mn>4</mn></mrow></mrow>'
    assert mpp.doprint(And(Eq(x, 3), Or(y < 3, x > y + 1))) == \
        '<mrow><mrow><mi>x</mi><mo>=</mo><mn>3</mn></mrow>'\
        '<mo>&#x2227;</mo><mrow><mo>(</mo><mrow><mrow><mi>x</mi><mo>></mo><mrow>'\
        '<mi>y</mi><mo>+</mo><mn>1</mn></mrow></mrow><mo>&#x2228;</mo><mrow>'\
        '<mi>y</mi><mo><</mo><mn>3</mn></mrow></mrow><mo>)</mo></mrow></mrow>'

    assert mpp.doprint(Not(x)) == '<mrow><mo>&#xAC;</mo><mi>x</mi></mrow>'
    assert mpp.doprint(Not(And(x, y))) == \
        '<mrow><mo>&#xAC;</mo><mrow><mo>(</mo><mrow><mi>x</mi><mo>&#x2227;</mo><mi>y</mi></mrow><mo>)</mo></mrow></mrow>'

