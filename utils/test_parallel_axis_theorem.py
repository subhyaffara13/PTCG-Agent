
def test_parallel_axis_theorem():
    # This tests the parallel axis theorem matrix by comparing to test
    # matrices.

    # First case, 1 in all directions.
    mat1 = Matrix(((2, -1, -1), (-1, 2, -1), (-1, -1, 2)))
    assert pat_matrix(1, 1, 1, 1) == mat1
    assert pat_matrix(2, 1, 1, 1) == 2*mat1

    # Second case, 1 in x, 0 in all others
    mat2 = Matrix(((0, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert pat_matrix(1, 1, 0, 0) == mat2
    assert pat_matrix(2, 1, 0, 0) == 2*mat2

    # Third case, 1 in y, 0 in all others
    mat3 = Matrix(((1, 0, 0), (0, 0, 0), (0, 0, 1)))
    assert pat_matrix(1, 0, 1, 0) == mat3
    assert pat_matrix(2, 0, 1, 0) == 2*mat3

    # Fourth case, 1 in z, 0 in all others
    mat4 = Matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))
    assert pat_matrix(1, 0, 0, 1) == mat4
    assert pat_matrix(2, 0, 0, 1) == 2*mat4

