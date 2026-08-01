
def sympy_is_channels_last_strides_3d(
    sizes: list[sympy.Basic], strides: list[sympy.Basic]
) -> sympy.Basic:
    return sympy_is_channels_last_strides_generic(sizes, strides, [1, 4, 3, 2, 0])

