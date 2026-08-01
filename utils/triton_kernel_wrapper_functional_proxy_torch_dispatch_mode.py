
def triton_kernel_wrapper_functional_proxy_torch_dispatch_mode(
    mode: ProxyTorchDispatchMode,
    *,
    kernel_idx: int,
    constant_args_idx: int,
    grid: list["TritonGridType"],
    tma_descriptor_metadata: TMADescriptorMetadata,
    kwargs: dict[str, Any],
    tensors_to_clone: list[str],
) -> dict[str, Any]:
    ret = trace_triton_kernel_wrapper(
        mode,
        triton_kernel_wrapper_functional,
        {
            "kernel_idx": kernel_idx,
            "constant_args_idx": constant_args_idx,
            "grid": grid,
            "tma_descriptor_metadata": tma_descriptor_metadata,
            "kwargs": kwargs,
            "tensors_to_clone": tensors_to_clone,
        },
    )
    if ret is None:
        raise AssertionError("trace_triton_kernel_wrapper returned None")
    return ret

