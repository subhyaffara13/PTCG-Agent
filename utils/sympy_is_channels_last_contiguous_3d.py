
def sympy_is_channels_last_contiguous_3d(
    sizes: list[sympy.Basic], strides: list[sympy.Basic]
) -> sympy.Basic:
    return sympy_is_contiguous_generic(sizes, strides, [1, 4, 3, 2, 0])

