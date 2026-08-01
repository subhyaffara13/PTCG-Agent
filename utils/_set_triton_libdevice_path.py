
def _set_triton_libdevice_path() -> None:
    """
    Use the CUDA toolkit's libdevice instead of Triton's bundled version.
    This ensures Triton's pow matches CUDA's powf for bitwise precision.
    Gated by config.eager_numerics.use_pytorch_libdevice.
    """
    from torch._inductor import config

    if not config.eager_numerics.use_pytorch_libdevice:
        return

    _set_triton_libdevice_path_impl()

