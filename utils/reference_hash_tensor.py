
def reference_hash_tensor(tensor, dim=(), keepdim=False, mode=0):
    if mode != 0:
        raise AssertionError(f"Only mode=0 (xor_sum) is supported right now, got mode={mode}")

    dtype = tensor.dtype
    if dtype.kind == 'f':
        tensor = tensor.astype(np.float64).view(np.uint64)
    else:
        tensor = tensor.astype(np.uint64)


    if dim == ():
        result = np.bitwise_xor.reduce(tensor.flatten(), keepdims=keepdim)
    else:
        if isinstance(dim, list):
            dim = tuple(dim)
        result = np.bitwise_xor.reduce(tensor, axis=dim, keepdims=keepdim)

    return result

