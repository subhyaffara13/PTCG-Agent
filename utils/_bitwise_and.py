
def _bitwise_and(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import BitwiseFn_bitwise_and

    return BitwiseFn_bitwise_and(a, b)

