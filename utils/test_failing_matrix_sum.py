
def test_failing_matrix_sum():
    n = Symbol('n')
    # TODO Implement matrix geometric series summation.
    A = Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    assert Sum(A ** n, (n, 1, 4)).doit() == \
        Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    # issue sympy/sympy#16989
    assert summation(A**n, (n, 1, 1)) == A

