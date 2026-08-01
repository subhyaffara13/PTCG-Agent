
def _matrix_derivative_old_algorithm(expr, x):
    from sympy.tensor.array.array_derivatives import ArrayDerivative
    lines = expr._eval_derivative_matrix_lines(x)

    parts = [i.build() for i in lines]

    from sympy.tensor.array.expressions.from_array_to_matrix import convert_array_to_matrix

    parts = [[convert_array_to_matrix(j) for j in i] for i in parts]

    def _get_shape(elem):
        if isinstance(elem, MatrixExpr):
            return elem.shape
        return 1, 1

    def get_rank(parts):
        return sum(j not in (1, None) for i in parts for j in _get_shape(i))

    ranks = [get_rank(i) for i in parts]
    rank = ranks[0]

    def contract_one_dims(parts):
        if len(parts) == 1:
            return parts[0]
        else:
            p1, p2 = parts[:2]
            if p2.is_Matrix:
                p2 = p2.T
            if p1 == Identity(1):
                pbase = p2
            elif p2 == Identity(1):
                pbase = p1
            else:
                pbase = p1*p2
            if len(parts) == 2:
                return pbase
            else:  # len(parts) > 2
                if pbase.is_Matrix:
                    raise ValueError("")
                return pbase*Mul.fromiter(parts[2:])

    if rank <= 2:
        return Add.fromiter([contract_one_dims(i) for i in parts])

    return ArrayDerivative(expr, x)

