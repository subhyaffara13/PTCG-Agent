
def transpose_(self, dim0, dim1):
    if self.layout in {
        torch.sparse_csr,
        torch.sparse_csc,
        torch.sparse_bsr,
        torch.sparse_bsc,
    }:
        raise AssertionError(
            f"torch.transpose_: in-place transposition is not supported for {self.layout} layout"
        )

    ndims = self.ndim

    dim0 = maybe_wrap_dim(dim0, ndims)
    dim1 = maybe_wrap_dim(dim1, ndims)

    if dim0 == dim1:
        return self

    size = list(self.size())
    stride = list(self.stride())

    stride[dim0], stride[dim1] = stride[dim1], stride[dim0]
    size[dim0], size[dim1] = size[dim1], size[dim0]

    self.as_strided_(size, stride)
    return self

