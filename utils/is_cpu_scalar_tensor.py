
def is_cpu_scalar_tensor(a: object) -> TypeGuard[TensorLike]:
    return isinstance(a, TensorLike) and a.ndim == 0 and a.device.type == "cpu"

