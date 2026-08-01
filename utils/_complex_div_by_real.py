
def _complex_div_by_real(z, den):
    """Divide complex by real using Python's method (two separate divisions).

    This ensures bit-exact compatibility with Python's complex division,
    avoiding C's multiply-by-reciprocal optimization that can cause 1 ULP differences
    on some platforms/compilers (e.g. clang on macOS arm64).

    https://github.com/fonttools/fonttools/issues/3928
    """
    zr = z.real
    zi = z.imag
    return complex(zr / den, zi / den)

