
def _einsum_dispatcher(*operands, out=None, optimize=None, **kwargs):
    # Arguably we dispatch on more arguments than we really should; see note in
    # _einsum_path_dispatcher for why.
    yield from operands
    yield out

