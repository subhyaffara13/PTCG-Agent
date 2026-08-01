
def squeeze_dims(li: list[int], dims: list[int]):
    if len(dims) == 0:
        return li
    wrapped_dims = _copy(dims)
    for i in range(len(dims)):
        wrapped_dims[i] = maybe_wrap_dim(wrapped_dims[i], len(li))
    result: list[int] = []
    for i in range(len(li)):
        if li[i] == 1:
            if i not in wrapped_dims:
                result.append(li[i])
        else:
            result.append(li[i])
    return result

