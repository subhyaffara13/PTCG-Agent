
def test_mathml_special_matrices():
    from sympy.matrices import Identity, ZeroMatrix, OneMatrix
    assert mathml(Identity(4), printer='presentation') == '<mi>&#x1D540;</mi>'
    assert mathml(ZeroMatrix(2, 2), printer='presentation') == '<mn>&#x1D7D8</mn>'
    assert mathml(OneMatrix(2, 2), printer='presentation') == '<mn>&#x1D7D9</mn>'

