
def test_mathml_SingularityFunction():
    assert mathml(SingularityFunction(x, 4, 5), printer='presentation') == \
        '<msup><mrow><mo>&#10216;</mo><mrow><mi>x</mi><mo>-</mo><mn>4</mn></mrow><mo>&#10217;</mo></mrow><mn>5</mn></msup>'
    assert mathml(SingularityFunction(x, -3, 4), printer='presentation') == \
        '<msup><mrow><mo>&#10216;</mo><mrow><mi>x</mi><mo>+</mo><mn>3</mn></mrow><mo>&#10217;</mo></mrow><mn>4</mn></msup>'
    assert mathml(SingularityFunction(x, 0, 4), printer='presentation') == \
        '<msup><mrow><mo>&#10216;</mo><mi>x</mi><mo>&#10217;</mo></mrow><mn>4</mn></msup>'
    assert mathml(SingularityFunction(x, a, n), printer='presentation') == \
        '<msup><mrow><mo>&#10216;</mo><mrow><mrow><mo>-</mo><mi>a</mi></mrow><mo>+</mo><mi>x</mi></mrow><mo>&#10217;</mo></mrow><mi>n</mi></msup>'
    assert mathml(SingularityFunction(x, 4, -2), printer='presentation') == \
        '<msup><mrow><mo>&#10216;</mo><mrow><mi>x</mi><mo>-</mo><mn>4</mn></mrow><mo>&#10217;</mo></mrow><mn>-2</mn></msup>'
    assert mathml(SingularityFunction(x, 4, -1), printer='presentation') == \
        '<msup><mrow><mo>&#10216;</mo><mrow><mi>x</mi><mo>-</mo><mn>4</mn></mrow><mo>&#10217;</mo></mrow><mn>-1</mn></msup>'

