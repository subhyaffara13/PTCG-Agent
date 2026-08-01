
def statically_launched_kernel_by_device(
    kernel: CompiledKernel, device_type: str = "cuda"
) -> StaticallyLaunchedTritonKernel:
    if device_type in ("cuda", "hip"):
        return StaticallyLaunchedCudaKernel(kernel)
    elif device_type == "xpu":
        return StaticallyLaunchedXpuKernel(kernel)
    else:
        raise NotImplementedError(
            f"Device type {device_type} is not supported for static launcher"
        )

