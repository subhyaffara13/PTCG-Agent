
def triton_kernel_wrap_(
    *,
    kernel_idx,
    constant_args_idx,
    grid,
    tma_descriptor_metadata,
    kwargs,
):
    from torch._higher_order_ops.triton_kernel_wrap import kernel_side_table

    constant_args = kernel_side_table.get_constant_args(constant_args_idx)
    ir.UserDefinedTritonKernel(
        kernel_idx=kernel_idx,
        grid=grid,
        tma_descriptor_metadata=tma_descriptor_metadata,
        kernel_args={**kwargs, **constant_args},
    )
    return {key: val for key, val in kwargs.items() if isinstance(val, TensorBox)}

