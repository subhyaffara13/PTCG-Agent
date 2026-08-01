
def inferUnsqueezeGeometry(tensor, dim):
    result_sizes = list(tensor.size())
    result_strides = list(tensor.stride())
    # pyrefly: ignore [unsupported-operation]
    new_stride = 1 if dim >= tensor.dim() else result_sizes[dim] * result_strides[dim]
    # pyrefly: ignore [bad-argument-type]
    result_sizes.insert(dim, 1)
    # pyrefly: ignore [bad-argument-type]
    result_strides.insert(dim, new_stride)
    return result_sizes, result_strides

