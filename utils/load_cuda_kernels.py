
def load_cuda_kernels():
    global mra_cuda_kernel
    if not is_kernels_available():
        raise ImportError("kernels is not installed, please install it with `pip install kernels`")
    from ...integrations.hub_kernels import get_kernel

    mra_cuda_kernel = get_kernel("kernels-community/mra")


def load_cuda_kernels():
    global lsh_cumulation
    if not is_kernels_available():
        raise ImportError("kernels is not installed, please install it with `pip install kernels`")
    from ...integrations.hub_kernels import get_kernel

    yoso = get_kernel("kernels-community/yoso")
    lsh_cumulation = yoso.lsh_cumulation

