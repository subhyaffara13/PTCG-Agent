
def test_simplify_matrix_expressions():
    # Various simplification functions
    assert type(gcd_terms(C*D + D*C)) == MatAdd
    a = gcd_terms(2*C*D + 4*D*C)
    assert type(a) == MatAdd
    assert a.args == (2*C*D, 4*D*C)

