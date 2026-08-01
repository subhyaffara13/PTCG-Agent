
def recover_orig_fp32_precision(fn):
    @contextlib.contextmanager
    def recover():
        old_mkldnn_conv_p = torch.backends.mkldnn.conv.fp32_precision  # type: ignore[attr-defined]
        old_mkldnn_rnn_p = torch.backends.mkldnn.rnn.fp32_precision  # type: ignore[attr-defined]
        old_mkldnn_matmul_p = torch.backends.mkldnn.matmul.fp32_precision  # type: ignore[attr-defined]
        old_cudnn_conv_p = torch.backends.cudnn.conv.fp32_precision  # type: ignore[attr-defined]
        old_cudnn_rnn_p = torch.backends.cudnn.rnn.fp32_precision  # type: ignore[attr-defined]
        old_cuda_matmul_p = torch.backends.cuda.matmul.fp32_precision
        try:
            yield
        finally:
            torch.backends.mkldnn.conv.fp32_precision = old_mkldnn_conv_p  # type: ignore[attr-defined]
            torch.backends.mkldnn.rnn.fp32_precision = old_mkldnn_rnn_p  # type: ignore[attr-defined]
            torch.backends.mkldnn.matmul.fp32_precision = old_mkldnn_matmul_p  # type: ignore[attr-defined]
            torch.backends.cudnn.conv.fp32_precision = old_cudnn_conv_p  # type: ignore[attr-defined]
            torch.backends.cudnn.rnn.fp32_precision = old_cudnn_rnn_p  # type: ignore[attr-defined]
            torch.backends.cuda.matmul.fp32_precision = old_cuda_matmul_p

    return recover()(fn)

