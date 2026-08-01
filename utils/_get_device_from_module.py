
def _get_device_from_module(module: str):
    last_part = module.rsplit(".", 1)[-1]
    if last_part in ["cuda", torch._C._get_privateuse1_backend_name(), "hpu"]:
        return last_part
    else:
        return "cpu"

