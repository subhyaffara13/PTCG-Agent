
def _matrix_derivative(expr, x, old_algorithm=False):

    if isinstance(expr, MatrixBase) or isinstance(x, MatrixBase):
        # Do not use array expressions for explicit matrices:
        old_algorithm = True

    if old_algorithm:
        return _matrix_derivative_old_algorithm(expr, x)

    from sympy.tensor.array.expressions.from_matrix_to_array import convert_matrix_to_array
    from sympy.tensor.array.expressions.arrayexpr_derivatives import array_derive
    from sympy.tensor.array.expressions.from_array_to_matrix import convert_array_to_matrix

    array_expr = convert_matrix_to_array(expr)
    diff_array_expr = array_derive(array_expr, x)
    diff_matrix_expr = convert_array_to_matrix(diff_array_expr)
    return diff_matrix_expr

