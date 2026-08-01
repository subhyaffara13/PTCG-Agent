
def test_pinv_succeeds_with_rank_decomposition_method():
    # Test rank decomposition method of pseudoinverse succeeding
    As = [Matrix([
        [61, 89, 55, 20, 71, 0],
        [62, 96, 85, 85, 16, 0],
        [69, 56, 17,  4, 54, 0],
        [10, 54, 91, 41, 71, 0],
        [ 7, 30, 10, 48, 90, 0],
        [0,0,0,0,0,0]])]
    for A in As:
        A_pinv = A.pinv(method="RD")
        AAp = A * A_pinv
        ApA = A_pinv * A
        assert simplify(AAp * A) == A
        assert simplify(ApA * A_pinv) == A_pinv
        assert AAp.H == AAp
        assert ApA.H == ApA

