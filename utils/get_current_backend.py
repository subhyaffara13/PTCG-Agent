
def get_current_backend(device_type: str | None = None) -> str:
    from torch._inductor.virtualized import V

    if not device_type:
        device_type = V.graph.get_current_device_or_throw().type
    if device_type == "cpu":
        return config.cpu_backend
    elif device_type == "mps":
        return "mps"
    elif device_type == "xpu":
        return config.xpu_backend
    elif device_type == "tpu":
        return config.tpu_backend
    else:
        return config.cuda_backend

