
def t_(self):
    ndims = self.ndim

    if self.is_sparse:
        sparse_dim = self.sparse_dim()
        dense_dim = self.dense_dim()
        if not (sparse_dim <= 2 and dense_dim == 0):
            raise AssertionError(
                f"t_ expects a tensor with <= 2 sparse and 0 dense dimensions, "
                f"but got {sparse_dim} sparse and {dense_dim} dense dimensions"
            )
    else:
        if self.dim() > 2:
            raise AssertionError(
                f"t_ expects a tensor with <= 2 dimensions, but self is {ndims}D"
            )

    return transpose_(self, 0, 0 if ndims < 2 else 1)

