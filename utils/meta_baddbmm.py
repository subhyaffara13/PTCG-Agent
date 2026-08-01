
def meta_baddbmm(self, batch1, batch2, *, beta=1, alpha=1):
    from torch.fx.experimental.symbolic_shapes import guard_or_true, sym_eq

    dim1 = batch1.size(0)
    dim2 = batch1.size(1)
    dim3 = batch2.size(2)
    if guard_or_true(torch.sym_not(sym_eq(self.shape, (dim1, dim2, dim3)))):
        self = self.expand((dim1, dim2, dim3))
    torch._check(batch1.dim() == 3, lambda: "batch1 must be a 3D tensor")
    torch._check(batch2.dim() == 3, lambda: "batch2 must be a 3D tensor")
    if not exp_config.skip_dtype_check_in_meta_registrations:
        torch._check(
            self.dtype == batch1.dtype == batch2.dtype,
            lambda: f"Input dtypes must be the same, got: input: {self.dtype}, batch1: {batch1.dtype}, batch2: {batch2.dtype}",
        )
    batch1_sizes = batch1.shape
    batch2_sizes = batch2.shape
    bs = batch1_sizes[0]
    contraction_size = batch1_sizes[2]
    torch._check(
        batch2_sizes[0] == bs and batch2_sizes[1] == contraction_size,
        lambda: (
            f"Expected size for first two dimensions of batch2 tensor to be: "
            f"[{bs}, {contraction_size}] but got: [{batch2_sizes[0]}, {batch2_sizes[1]}]."
        ),
    )
    return self.new_empty(self.size())

