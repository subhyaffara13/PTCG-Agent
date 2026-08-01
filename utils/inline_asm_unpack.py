
def inline_asm_unpack(x, orig, pack: tl.constexpr):
    """Unpad and reshape back to orig's shape."""
    result = x
    n_pad: tl.constexpr = _log2(pack) - _log2(orig.numel)
    for _ in tl.static_range(n_pad):
        result, _ = tl.split(tl.reshape(result, (result.shape[0] // 2, 2)))
    return tl.reshape(result, orig.shape)

