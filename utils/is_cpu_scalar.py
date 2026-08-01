
def is_cpu_scalar(x: TensorLikeType) -> bool:
    return x.dim() == 0 and x.device.type == "cpu"

