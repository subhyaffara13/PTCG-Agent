
def test_mathml_presentation_numbers():
    n = Symbol('n')
    assert mathml(catalan(n), printer='presentation') == \
        '<msub><mi>C</mi><mi>n</mi></msub>'
    assert mathml(bernoulli(n), printer='presentation') == \
        '<msub><mi>B</mi><mi>n</mi></msub>'
    assert mathml(bell(n), printer='presentation') == \
        '<msub><mi>B</mi><mi>n</mi></msub>'
    assert mathml(euler(n), printer='presentation') == \
        '<msub><mi>E</mi><mi>n</mi></msub>'
    assert mathml(fibonacci(n), printer='presentation') == \
        '<msub><mi>F</mi><mi>n</mi></msub>'
    assert mathml(lucas(n), printer='presentation') == \
        '<msub><mi>L</mi><mi>n</mi></msub>'
    assert mathml(tribonacci(n), printer='presentation') == \
        '<msub><mi>T</mi><mi>n</mi></msub>'
    assert mathml(bernoulli(n, x), printer='presentation') == \
        mathml(bell(n, x), printer='presentation') == \
        '<mrow><msub><mi>B</mi><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(euler(n, x), printer='presentation') == \
        '<mrow><msub><mi>E</mi><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(fibonacci(n, x), printer='presentation') == \
        '<mrow><msub><mi>F</mi><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
    assert mathml(tribonacci(n, x), printer='presentation') == \
        '<mrow><msub><mi>T</mi><mi>n</mi></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'

