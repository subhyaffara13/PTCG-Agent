
def device_put_noop(x, device, non_blocking=True):
    return x.device == decode_device(device)

