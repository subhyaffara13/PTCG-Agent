
def is_fp16_enabled(device_type):
    # Autocast world
    autocast_dtype = torch.get_autocast_dtype(device_type)
    fp16_enabled = autocast_dtype == torch.float16
    fp16_enabled = fp16_enabled and torch.is_autocast_enabled(device_type)

    return fp16_enabled

