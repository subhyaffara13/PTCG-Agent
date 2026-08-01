
def is_mkldnn_fp16_supported(device_type: str) -> bool:
    """
    Returns True if the device supports MKL-DNN FP16.
    """
    if device_type == "cpu":
        return torch.ops.mkldnn._is_mkldnn_fp16_supported()
    elif "xpu" in device_type:
        # match "xpu", "xpu:0", "xpu:1", etc.
        return True
    return False

