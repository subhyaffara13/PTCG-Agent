
def sympify_mpmath_matrix(arg):
    mat = [_sympify(x) for x in arg]
    return ImmutableDenseMatrix(arg.rows, arg.cols, mat)

