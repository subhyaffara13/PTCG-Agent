from typing import Any

def as_numpy_array(array: Array, *, xp: ModuleType) -> np.typing.NDArray[Any]:
    """
    Convert array to NumPy, bypassing GPU-CPU transfer guards and densification guards.
    """
    if is_cupy_namespace(xp):
        return xp.asnumpy(array)
    if is_pydata_sparse_namespace(xp):
        return array.todense()  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]

    if is_torch_namespace(xp):
        array = to_device(array, "cpu")
    if is_array_api_strict_namespace(xp):
        cpu: Device = xp.Device("CPU_DEVICE")
        array = to_device(array, cpu)
    if is_jax_namespace(xp):
        import jax

        # Note: only needed if the transfer guard is enabled
        cpu = cast(Device, jax.devices("cpu")[0])
        array = to_device(array, cpu)

    return np.asarray(array)

