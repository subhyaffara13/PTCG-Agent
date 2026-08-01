
def out_dtype_decomp(*args, **kwargs):
    from torch._higher_order_ops.out_dtype import out_dtype_dense

    return out_dtype_dense(*args, **kwargs)

