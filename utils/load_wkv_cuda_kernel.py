
def load_wkv_cuda_kernel(context_length):
    global rwkv_cuda_kernel
    if not is_kernels_available():
        raise ImportError("kernels is not installed, please install it with `pip install kernels`")

    from ...integrations.hub_kernels import get_kernel

    rwkv_cuda_kernel = get_kernel("kernels-community/rwkv")
    rwkv_cuda_kernel.max_seq_length = context_length

