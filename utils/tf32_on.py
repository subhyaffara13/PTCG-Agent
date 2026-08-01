
def tf32_on(self, tf32_precision=1e-5):
    old_allow_tf32_matmul = torch.backends.cuda.matmul.allow_tf32
    old_precision = self.precision
    try:
        torch.backends.cuda.matmul.allow_tf32 = True
        self.precision = tf32_precision
        with torch.backends.cudnn.flags(enabled=None, benchmark=None, deterministic=None, allow_tf32=True):
            yield
    finally:
        torch.backends.cuda.matmul.allow_tf32 = old_allow_tf32_matmul
        self.precision = old_precision


def tf32_on(self, tf32_precision=1e-5):
    old_matmul_precision = torch.backends.mkldnn.matmul.fp32_precision
    old_conv_precision = torch.backends.mkldnn.conv.fp32_precision
    old_precision = self.precision
    try:
        torch.backends.mkldnn.matmul.fp32_precision = "tf32"
        torch.backends.mkldnn.conv.fp32_precision = "tf32"
        self.precision = tf32_precision
        yield
    finally:
        torch.backends.mkldnn.matmul.fp32_precision = old_matmul_precision
        torch.backends.mkldnn.conv.fp32_precision = old_conv_precision
        self.precision = old_precision

