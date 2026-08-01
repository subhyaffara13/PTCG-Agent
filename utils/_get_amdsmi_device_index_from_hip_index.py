
def _get_amdsmi_device_index_from_hip_index(device: int) -> int:
    r"""Return amdsmi index from HIP device index. They are not always the same.

    Assume amdsmi_init() already completes successfully."""
    global _cached_hip_to_amdsmi
    if _cached_hip_to_amdsmi is None:
        amdsmi_handles = amdsmi.amdsmi_get_processor_handles()

        def gen():
            for amdsmi_idx, handle in enumerate(amdsmi_handles):
                info = amdsmi.amdsmi_get_gpu_enumeration_info(handle)
                if "hip_id" in info:
                    yield info["hip_id"], amdsmi_idx

        _cached_hip_to_amdsmi = dict(gen())
        if not _cached_hip_to_amdsmi and len(amdsmi_handles) > 1:
            warnings.warn(
                "Cannot translate HIP ID to AMD SMI ID due to"
                " lack of translation information prior to ROCm 6.4."
                " Functions that rely on amdsmi"
                " (e.g. temperature()) may operate on wrong devices."
            )
    if device not in _cached_hip_to_amdsmi:
        warnings.warn(
            f"Cannot translate HIP ID {device} to AMD SMI ID due to"
            " undetected HIP ID from amdsmi."
            " amdsmi_get_gpu_enumeration_info() only report these HIP IDs"
            f" {list(_cached_hip_to_amdsmi.keys())}."
            " Functions that rely on amdsmi"
            " (e.g. temperature()) may operate on wrong devices."
        )
    return _cached_hip_to_amdsmi.get(device, device)

