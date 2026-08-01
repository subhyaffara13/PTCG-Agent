
def get_shape_from_sympy_shape(sympy_shape):
    return [None if i is None else (int(i) if is_literal(i) else str(i)) for i in sympy_shape]

