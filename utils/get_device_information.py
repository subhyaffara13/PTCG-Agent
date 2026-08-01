
def get_device_information(device_type: str) -> dict[str, str]:
    """
    Gets all the current device information used to compile the .so.
    """
    metadata: dict[str, str] = {
        "AOTI_PLATFORM": sys.platform,
        "AOTI_MACHINE": platform.machine(),
        "AOTI_CPU_ISA": str(torch._inductor.cpu_vec_isa.pick_vec_isa()).upper(),
        "AOTI_COMPUTE_CAPABILITY": str(
            get_interface_for_device(device_type).get_compute_capability()
        ),
    }
    return metadata

