
def _get_amdsmi_power_draw(device: Device = None) -> int:
    handle = _get_amdsmi_handler(device)
    socket_power = amdsmi.amdsmi_get_power_info(handle)["average_socket_power"]
    if socket_power != "N/A":
        return socket_power
    else:
        socket_power = amdsmi.amdsmi_get_power_info(handle)["current_socket_power"]
        if socket_power != "N/A":
            return socket_power
        else:
            return 0

