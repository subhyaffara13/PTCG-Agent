
def is_habana_gaudi1() -> bool:
    if not is_torch_hpu_available():
        return False

    import habana_frameworks.torch.utils.experimental as htexp

    # Check if the device is Gaudi1 (vs Gaudi2, Gaudi3)
    return htexp._get_device_type() == htexp.synDeviceType.synDeviceGaudi

