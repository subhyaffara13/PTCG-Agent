
def gather_shape_check(self, dim, index):
    self_dims = max(self.dim(), 1)
    index_dims = max(index.dim(), 1)
    torch._check(
        self_dims == index_dims,
        lambda: "Index tensor must have the same number of dimensions as input tensor",
    )
    for i in range(self_dims):
        if i != dim:
            torch._check(
                ensure_nonempty_size(index, i) <= ensure_nonempty_size(self, i),
                lambda: f"Size does not match at dimension {i} expected index {index.shape}"
                + f" to be no larger than self {self.shape} apart from dimension {dim}",
            )

