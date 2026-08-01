
def test_pinv_rank_deficient():
    # Test the four properties of the pseudoinverse for various matrices.
    As = [Matrix([[1, 1, 1], [2, 2, 2]]),
          Matrix([[1, 0], [0, 0]]),
          Matrix([[1, 2], [2, 4], [3, 6]])]

    for A in As:
        A_pinv = A.pinv(method="RD")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

    for A in As:
        A_pinv = A.pinv(method="ED")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

    # Test solving with rank-deficient matrices.
    A = Matrix([[1, 0], [0, 0]])
    # Exact, non-unique solution.
    B = Matrix([3, 0])
    solution = A.pinv_solve(B)
    w1 = solution.atoms(Symbol).pop()
    assert w1.name == 'w1_0'
    assert solution == Matrix([3, w1])
    assert A * A.pinv() * B == B
    # Least squares, non-unique solution.
    B = Matrix([3, 1])
    solution = A.pinv_solve(B)
    w1 = solution.atoms(Symbol).pop()
    assert w1.name == 'w1_0'
    assert solution == Matrix([3, w1])
    assert A * A.pinv() * B != B

