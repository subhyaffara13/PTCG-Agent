
def reduced_f32_off():
    old_matmul_precision = torch.backends.mkldnn.matmul.fp32_precision
    old_conv_precision = torch.backends.mkldnn.conv.fp32_precision
    try:
        torch.backends.mkldnn.matmul.fp32_precision = "ieee"
        torch.backends.mkldnn.conv.fp32_precision = "ieee"
        yield
    finally:
        torch.backends.mkldnn.matmul.fp32_precision = old_matmul_precision
        torch.backends.mkldnn.conv.fp32_precision = old_conv_precision

