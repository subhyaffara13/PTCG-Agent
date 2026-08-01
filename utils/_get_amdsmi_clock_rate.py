
def _get_amdsmi_clock_rate(device: Device = None) -> int:
    handle = _get_amdsmi_handler(device)
    clock_info = amdsmi.amdsmi_get_clock_info(handle, amdsmi.AmdSmiClkType.GFX)
    if "cur_clk" in clock_info:  # ROCm 6.2 deprecation
        clock_rate = clock_info["cur_clk"]
    else:
        clock_rate = clock_info["clk"]
    if clock_rate != "N/A":
        return clock_rate
    else:
        return 0

