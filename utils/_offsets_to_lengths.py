
def _offsets_to_lengths(offsets, max_len):
    """
    If the offsets tensor is fake, then we don't know the actual lengths.
    In that case, we can just assume the worst case; each batch has max length.
    """
    from torch._subclasses.fake_tensor import FakeTensor
    from torch._subclasses.functional_tensor import FunctionalTensor
    if not isinstance(offsets, (FakeTensor, FunctionalTensor)) and offsets.device.type != "meta":
        return offsets.diff().tolist()
    return [max_len] * (offsets.size(0) - 1)

