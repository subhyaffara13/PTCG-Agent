
def common_meta_baddbmm_bmm(batch1, batch2, is_bmm, self_baddbmm=None, out_dtype=None):
    from torch.fx.experimental.symbolic_shapes import sym_and, sym_eq

    torch._check(batch1.dim() == 3, lambda: "batch1 must be a 3D tensor")
    torch._check(batch2.dim() == 3, lambda: "batch2 must be a 3D tensor")
    torch._check(
        batch1.dtype == batch2.dtype,
        lambda: f"expected scalar type {batch1.dtype} but found {batch2.dtype}",
    )

    batch1_sizes = batch1.size()
    batch2_sizes = batch2.size()

    bs = batch1_sizes[0]
    contraction_size = batch1_sizes[2]
    res_rows = batch1_sizes[1]
    res_cols = batch2_sizes[2]
    output_size = (bs, res_rows, res_cols)

    torch._check(
        sym_and(sym_eq(batch2_sizes[0], bs), sym_eq(batch2_sizes[1], contraction_size)),
        lambda: f"Expected size for first two dimensions of batch2 tensor to be: [{bs}"
        f", {contraction_size}] but got: [{batch2_sizes[0]}, {batch2_sizes[1]}].",
    )
    if out_dtype:
        supported_out_dtype = (
            batch1.dtype == torch.float16 or batch1.dtype == torch.bfloat16
        ) and out_dtype == torch.float32
        torch._check(
            out_dtype == batch1.dtype or supported_out_dtype,
            lambda: "out_dtype only supported for torch.float32 output with float16/bfloat16 inputs or same as input dtypes",
        )
        output = batch2.new_empty(output_size).to(out_dtype)
    else:
        # TODO: handle out
        output = batch2.new_empty(output_size)

    if not is_bmm and self_baddbmm is not None:
        torch._check(self_baddbmm.dim() == 3, lambda: "self must be a 3D tensor")
        torch._check(
            sym_eq(self_baddbmm.size(), output_size),
            lambda: f"Expected an input tensor shape with shape {output_size} but got shape: {self_baddbmm.size()}",
        )

    return output

