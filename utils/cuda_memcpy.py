
def cuda_memcpy(dst, src):
    from cuda import cudart  # noqa: PLC0415

    cudart.cudaMemcpy(
        dst.data_ptr(),
        src.data_ptr(),
        src.element_size() * src.nelement(),
        cudart.cudaMemcpyKind.cudaMemcpyDeviceToDevice,
    )

