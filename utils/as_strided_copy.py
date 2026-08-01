
def as_strided_copy(x, size, stride, storage_offset=None):
    result = as_strided(x, size, stride, storage_offset)
    return clone(result)

