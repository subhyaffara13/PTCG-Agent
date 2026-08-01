
def out_dtype_fake_tensor_mode(
    mode: FakeTensorMode,
    op: torch._ops.OpOverload,
    output_dtype: torch.dtype,
    *args,
):
    with mode:
        return out_dtype_dense(op, output_dtype, *args)

