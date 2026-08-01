
def get_scheduling_for_device(device: str) -> SchedulingConstructor | None:
    return device_codegens[device].scheduling if device in device_codegens else None

