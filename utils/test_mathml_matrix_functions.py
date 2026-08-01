
def test_mathml_matrix_functions():
    from sympy.matrices import Adjoint, Inverse, Transpose
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert mathml(Adjoint(X), printer='presentation') == \
        '<msup><mi>X</mi><mo>&#x2020;</mo></msup>'
    assert mathml(Adjoint(X + Y), printer='presentation') == \
        '<msup><mrow><mo>(</mo><mrow><mi>X</mi><mo>+</mo><mi>Y</mi></mrow><mo>)</mo></mrow><mo>&#x2020;</mo></msup>'
    assert mathml(Adjoint(X) + Adjoint(Y), printer='presentation') == \
        '<mrow><msup><mi>X</mi><mo>&#x2020;</mo></msup><mo>+</mo><msup>' \
        '<mi>Y</mi><mo>&#x2020;</mo></msup></mrow>'
    assert mathml(Adjoint(X*Y), printer='presentation') == \
        '<msup><mrow><mo>(</mo><mrow><mi>X</mi><mo>&InvisibleTimes;</mo>' \
        '<mi>Y</mi></mrow><mo>)</mo></mrow><mo>&#x2020;</mo></msup>'
    assert mathml(Adjoint(Y)*Adjoint(X), printer='presentation') == \
        '<mrow><msup><mi>Y</mi><mo>&#x2020;</mo></msup><mo>&InvisibleTimes;' \
        '</mo><msup><mi>X</mi><mo>&#x2020;</mo></msup></mrow>'
    assert mathml(Adjoint(X**2), printer='presentation') == \
        '<msup><mrow><mo>(</mo><msup><mi>X</mi><mn>2</mn></msup><mo>)</mo></mrow><mo>&#x2020;</mo></msup>'
    assert mathml(Adjoint(X)**2, printer='presentation') == \
        '<msup><mrow><mo>(</mo><msup><mi>X</mi><mo>&#x2020;</mo></msup><mo>)</mo></mrow><mn>2</mn></msup>'
    assert mathml(Adjoint(Inverse(X)), printer='presentation') == \
        '<msup><mrow><mo>(</mo><msup><mi>X</mi><mn>-1</mn></msup><mo>)</mo></mrow><mo>&#x2020;</mo></msup>'
    assert mathml(Inverse(Adjoint(X)), printer='presentation') == \
        '<msup><mrow><mo>(</mo><msup><mi>X</mi><mo>&#x2020;</mo></msup><mo>)</mo></mrow><mn>-1</mn></msup>'
    assert mathml(Adjoint(Transpose(X)), printer='presentation') == \
        '<msup><mrow><mo>(</mo><msup><mi>X</mi><mo>T</mo></msup><mo>)</mo></mrow><mo>&#x2020;</mo></msup>'
    assert mathml(Transpose(Adjoint(X)), printer='presentation') ==  \
        '<msup><mrow><mo>(</mo><msup><mi>X</mi><mo>&#x2020;</mo></msup><mo>)</mo></mrow><mo>T</mo></msup>'
    assert mathml(Transpose(Adjoint(X) + Y), printer='presentation') ==  \
        '<msup><mrow><mo>(</mo><mrow><msup><mi>X</mi><mo>&#x2020;</mo></msup>' \
        '<mo>+</mo><mi>Y</mi></mrow><mo>)</mo></mrow><mo>T</mo></msup>'
    assert mathml(Transpose(X), printer='presentation') == \
        '<msup><mi>X</mi><mo>T</mo></msup>'
    assert mathml(Transpose(X + Y), printer='presentation') == \
        '<msup><mrow><mo>(</mo><mrow><mi>X</mi><mo>+</mo><mi>Y</mi></mrow><mo>)</mo></mrow><mo>T</mo></msup>'

