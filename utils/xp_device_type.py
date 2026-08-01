
def xp_device_type(a: Array) -> Literal["cpu", "cuda", None]:
    if is_numpy_array(a):
        return "cpu"
    if is_cupy_array(a):
        return "cuda"
    if is_torch_array(a):
        # TODO this can return other backends e.g. tpu but they're unsupported in scipy
        return a.device.type
    if is_jax_array(a):
        # TODO this can return other backends e.g. tpu but they're unsupported in scipy
        return "cuda" if (p := a.device.platform) == "gpu" else p
    if is_dask_array(a):
        return xp_device_type(a._meta)
    # array-api-strict is a stand-in for unknown libraries; don't special-case it
    return None

