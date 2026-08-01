
def scatter_shape_check(self, dim, index, src_opt=None):
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    if guard_or_false(index.numel() == 0):
        return
    torch._check(
        ensure_nonempty_dim(self.dim()) == ensure_nonempty_dim(index.dim()),
        lambda: "Index tensor must have the same number of dimensions as self tensor",
    )

    self_dims = ensure_nonempty_dim(self.dim())

    # Check: index.size(d) <= self.size(d) for all d != dim
    # Use torch._check to defer validation to runtime for unbacked symbols.
    for d in range(self_dims):
        if d == dim:
            continue
        index_d_size = ensure_nonempty_size(index, d)
        self_d_size = ensure_nonempty_size(self, d)
        torch._check(
            index_d_size <= self_d_size,
            lambda: f"Expected index {index.shape} to be no larger than self {self.shape}"
            + f" apart from dimension {dim}",
        )

    # Check: index.size(d) <= src.size(d) for all d if src is Tensor
    if src_opt is not None:
        torch._check(
            ensure_nonempty_dim(self.dim()) == ensure_nonempty_dim(src_opt.dim()),
            lambda: "Index tensor must have the same number of dimensions as src tensor",
        )
        for d in range(self_dims):
            index_d_size = ensure_nonempty_size(index, d)
            src_d_size = ensure_nonempty_size(src_opt, d)
            torch._check(
                index_d_size <= src_d_size,
                lambda: f"Expected index {index.shape} to be no larger than src {src_opt.shape}",
            )

