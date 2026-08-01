
def ptr_stride_extractor(*tensors):
    for t in tensors:
        yield t
        yield from t.stride()

