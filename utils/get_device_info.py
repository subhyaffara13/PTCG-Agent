
def get_device_info(an_id):
    """returns information about a midi device
    pygame.midi.get_device_info(an_id): return (interf, name,
                                                input, output,
                                                opened)

    interf - a byte string describing the device interface, eg b'ALSA'.
    name - a byte string for the name of the device, eg b'Midi Through Port-0'
    input - 0, or 1 if the device is an input device.
    output - 0, or 1 if the device is an output device.
    opened - 0, or 1 if the device is opened.

    If the id is out of range, the function returns None.
    """
    _check_init()
    return _pypm.GetDeviceInfo(an_id)


def get_device_info(silent=True) -> str:
    machine = MachineInfo(silent)
    info = machine.machine_info
    if info:
        info = {key: value for key, value in info.items() if key in ["gpu", "cpu", "memory"]}
    return json.dumps(info, indent=2)

