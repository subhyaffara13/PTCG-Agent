
def test_octave_matrix_elements():
    A = Matrix([[x, 2, x*y]])
    assert mcode(A[0, 0]**2 + A[0, 1] + A[0, 2]) == "x.^2 + x.*y + 2"
    A = MatrixSymbol('AA', 1, 3)
    assert mcode(A) == "AA"
    assert mcode(A[0, 0]**2 + sin(A[0,1]) + A[0,2]) == \
           "sin(AA(1, 2)) + AA(1, 1).^2 + AA(1, 3)"
    assert mcode(sum(A)) == "AA(1, 1) + AA(1, 2) + AA(1, 3)"

