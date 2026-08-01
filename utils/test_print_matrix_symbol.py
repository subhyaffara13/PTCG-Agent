
def test_print_matrix_symbol():
    A = MatrixSymbol('A', 1, 2)
    assert mpp.doprint(A) == '<mi>A</mi>'
    assert mp.doprint(A) == '<ci>A</ci>'
    assert mathml(A, printer='presentation', mat_symbol_style="bold") == \
        '<mi mathvariant="bold">A</mi>'
    # No effect in content printer
    assert mathml(A, mat_symbol_style="bold") == '<ci>A</ci>'

