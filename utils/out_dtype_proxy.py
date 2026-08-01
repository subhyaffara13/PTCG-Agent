
def out_dtype_proxy(
    mode: ProxyTorchDispatchMode,
    op: torch._ops.OpOverload,
    output_dtype: torch.dtype,
    *args,
):
    return trace_out_dtype(mode, out_dtype, op, output_dtype, *args)

