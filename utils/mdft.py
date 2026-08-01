
def mdft(n):
    r"""
    .. deprecated:: 1.9

       Use DFT from sympy.matrices.expressions.fourier instead.

       To get identical behavior to ``mdft(n)``, use ``DFT(n).as_explicit()``.
    """
    from sympy.matrices.expressions.fourier import DFT
    return DFT(n).as_mutable()

