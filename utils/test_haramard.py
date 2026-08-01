
def test_haramard():
    A = MatrixSymbol('A', 3, 3)
    B = MatrixSymbol('B', 3, 3)
    v = MatrixSymbol('v', 3, 1)
    h = MatrixSymbol('h', 1, 3)
    C = HadamardProduct(A, B)
    assert julia_code(C) == "A .* B"
    assert julia_code(C*v) == "(A .* B) * v"
    assert julia_code(h*C*v) == "h * (A .* B) * v"
    assert julia_code(C*A) == "(A .* B) * A"
    # mixing Hadamard and scalar strange b/c we vectorize scalars
    assert julia_code(C*x*y) == "(x .* y) * (A .* B)"

