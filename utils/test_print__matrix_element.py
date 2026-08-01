
def test_print_MatrixElement():
    i, j = symbols('i j')
    A = MatrixSymbol('A', i, j)
    assert mathml(A[0,0],printer = 'presentation') == \
        '<msub><mi>A</mi><mrow><mn>0</mn><mo>,</mo><mn>0</mn></mrow></msub>'
    assert mathml(A[i,j], printer = 'presentation') == \
        '<msub><mi>A</mi><mrow><mi>i</mi><mo>,</mo><mi>j</mi></mrow></msub>'
    assert mathml(A[i*j,0], printer = 'presentation') == \
        '<msub><mi>A</mi><mrow><mrow><mi>i</mi><mo>&InvisibleTimes;</mo><mi>j</mi></mrow><mo>,</mo><mn>0</mn></mrow></msub>'

