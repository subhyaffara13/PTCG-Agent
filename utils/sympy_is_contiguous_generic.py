
def sympy_is_contiguous_generic(
    sizes: list[sympy.Basic], strides: list[sympy.Basic], dim_order: list[int]
) -> sympy.Basic:
    import sympy

    dim = len(sizes)

    if len(dim_order) != dim:
        return sympy.false

    is_contiguous = sympy.true
    z = sympy.S.One
    # Contiguous if the strides make sense (or the dim is size 1)
    for d in dim_order:
        is_contiguous &= sympy.Eq(sizes[d], sympy.S.One) | sympy.Eq(strides[d], z)
        z *= sizes[d]
    # OR if any size is zero
    for d in range(dim):
        is_contiguous |= sympy.Eq(sizes[d], sympy.S.Zero)
    return is_contiguous

