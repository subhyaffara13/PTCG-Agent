
def inline_asm_pack(x, pack: tl.constexpr):
    """Ravel to 1D and pad (via join with zeros) so numel is divisible by pack."""
    result = x.ravel()
    # Only pad when the block size is smaller than pack. When block >= pack
    # the numel is already divisible by pack (both are powers of 2).
    n_pad: tl.constexpr = _log2(pack) - _log2(result.numel)
    for _ in tl.static_range(n_pad):
        result = tl.reshape(
            tl.join(result, tl.zeros_like(result)), (result.shape[0] * 2,)
        )
    return result

