
def sympy_is_contiguous(
    sizes: list[sympy.Basic], strides: list[sympy.Basic]
) -> sympy.Basic:
    dim = len(sizes)
    return sympy_is_contiguous_generic(sizes, strides, list(range(dim - 1, -1, -1)))

