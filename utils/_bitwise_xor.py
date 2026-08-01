
def _bitwise_xor(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import BitwiseFn_bitwise_xor

    return BitwiseFn_bitwise_xor(a, b)

