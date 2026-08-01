
def test_print_hadamard():
    from sympy.matrices.expressions import HadamardProduct
    from sympy.matrices.expressions import Transpose

    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)

    assert mathml(HadamardProduct(X, Y*Y), printer="presentation") == \
        '<mrow>' \
        '<mi>X</mi>' \
        '<mo>&#x2218;</mo>' \
        '<msup><mi>Y</mi><mn>2</mn></msup>' \
        '</mrow>'

    assert mathml(HadamardProduct(X, Y)*Y, printer="presentation") == \
        '<mrow>' \
        '<mrow><mo>(</mo>' \
        '<mrow><mi>X</mi><mo>&#x2218;</mo><mi>Y</mi></mrow>' \
        '<mo>)</mo></mrow>' \
        '<mo>&InvisibleTimes;</mo><mi>Y</mi>' \
        '</mrow>'

    assert mathml(HadamardProduct(X, Y, Y), printer="presentation") == \
        '<mrow>' \
        '<mi>X</mi><mo>&#x2218;</mo>' \
        '<mi>Y</mi><mo>&#x2218;</mo>' \
        '<mi>Y</mi>' \
        '</mrow>'

    assert mathml(
        Transpose(HadamardProduct(X, Y)), printer="presentation") == \
            '<msup>' \
            '<mrow><mo>(</mo>' \
            '<mrow><mi>X</mi><mo>&#x2218;</mo><mi>Y</mi></mrow>' \
            '<mo>)</mo></mrow>' \
            '<mo>T</mo>' \
            '</msup>'

