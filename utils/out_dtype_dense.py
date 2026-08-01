
def out_dtype_dense(op: torch._ops.OpOverload, output_dtype: torch.dtype, *args):
    if is_int_mm(op, output_dtype, args):
        return torch._int_mm(*args)
    return out_dtype_fallback(op, output_dtype, *args)

