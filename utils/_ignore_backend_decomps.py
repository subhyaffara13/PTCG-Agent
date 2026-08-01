
def _ignore_backend_decomps():
    orig_mkldnn_flag = torch.backends.mkldnn.set_flags(False)
    orig_nnpack_flag = torch.backends.nnpack.set_flags(False)
    orig_cudnn_flag = torch.backends.cudnn.set_flags(False)

    try:
        yield
    finally:
        torch.backends.mkldnn.set_flags(*orig_mkldnn_flag)
        torch.backends.nnpack.set_flags(*orig_nnpack_flag)
        torch.backends.cudnn.set_flags(*orig_cudnn_flag)

