
def has_triton_experimental_host_tma() -> bool:
    if has_triton_package():
        if _device_supports_tma():
            try:
                from triton.tools.experimental_descriptor import (  # noqa: F401
                    create_1d_tma_descriptor,
                    create_2d_tma_descriptor,
                )

                try:
                    from triton.tools.experimental_descriptor import enable_in_pytorch

                    return enable_in_pytorch()
                except ImportError:
                    return True
            except ImportError:
                pass

    return False

