
def _gen_rank_device(global_rank: int, device_type: str = "cuda") -> str:
    if device_type == "cpu":
        return "cpu"
    device_module = _get_device_module(device_type)
    if device_module.is_available():
        return _normalize_device_info(
            device_type, global_rank % device_module.device_count()
        )
    return "cpu"

