
def tf32_is_not_fp32():
    if not torch.backends.mkldnn.is_available():
        return False
    if not torch.cpu._is_amx_fp16_supported():
        return False
    return True

