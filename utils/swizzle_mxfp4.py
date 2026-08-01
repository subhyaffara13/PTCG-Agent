
def swizzle_mxfp4(w, w_scale, triton_kernels_hub):
    """
    Changes the layout of the tensors depending on the hardware
    """
    FP4, convert_layout, wrap_torch_tensor = (
        triton_kernels_hub.tensor.FP4,
        triton_kernels_hub.tensor.convert_layout,
        triton_kernels_hub.tensor.wrap_torch_tensor,
    )
    layout = triton_kernels_hub.tensor_details.layout
    StridedLayout = triton_kernels_hub.tensor_details.layout.StridedLayout

    value_layout, value_layout_opts = layout.make_default_matmul_mxfp4_w_layout(mx_axis=1)
    w = convert_layout(wrap_torch_tensor(w, dtype=FP4), value_layout, **value_layout_opts)
    w_scale = convert_layout(wrap_torch_tensor(w_scale), StridedLayout)
    return w, w_scale

