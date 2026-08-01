
def _cast_if_autocast_enabled(device_type, *args):
    if not torch.is_autocast_enabled():
        return args
    else:
        target_dtype = torch.get_autocast_dtype(device_type)
        return torch.amp.autocast_mode._cast(args, device_type, target_dtype)

