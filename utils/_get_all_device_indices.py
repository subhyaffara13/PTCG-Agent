
def _get_all_device_indices():
    # all device index
    return _get_device_attr(lambda m: list(range(m.device_count())))

