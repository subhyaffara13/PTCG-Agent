
def typecast_tensors(tensors, target_dtype, casting):
    return tuple(typecast_tensor(t, target_dtype, casting) for t in tensors)

