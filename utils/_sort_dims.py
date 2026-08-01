
def _sort_dims(self: Tensor, dim: list[int], exclude_last: bool = False):
    sorted_dims = list(dim)
    self_strides = self.stride()
    end = len(sorted_dims) - int(exclude_last)
    sorted_dims[:end] = sorted(
        sorted_dims[:end], key=lambda i: self_strides[i], reverse=True
    )
    return sorted_dims

