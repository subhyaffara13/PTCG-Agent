
def test_issue_16577():
    assert linear_eq_to_matrix(Eq(a*(2*x + 3*y) + 4*y, 5), x, y) == (
        Matrix([[2*a, 3*a + 4]]), Matrix([[5]]))

