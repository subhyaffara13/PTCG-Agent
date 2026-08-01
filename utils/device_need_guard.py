
def device_need_guard(device: str) -> bool:
    return device != "mps" and is_gpu(device)  # TODO: MPS does not expose streams now

