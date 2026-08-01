
def get_count():
    """gets the number of devices.
    pygame.midi.get_count(): return num_devices


    Device ids range from 0 to get_count() -1
    """
    _check_init()
    return _pypm.CountDevices()

