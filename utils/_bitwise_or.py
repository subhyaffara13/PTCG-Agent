
def _bitwise_or(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import BitwiseFn_bitwise_or

    return BitwiseFn_bitwise_or(a, b)

