
def _get_current_device_index():
    # current device index
    return _get_device_attr(lambda m: m.current_device())

