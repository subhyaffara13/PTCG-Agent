
def _array_api_array_conversion(
    value: Array, xp: ModuleType, device: Device | None = None
) -> Array:
    """Convert an Array API compatible array to the specified xp module array type."""
    try:
        x = xp.from_dlpack(value)
        return to_device(x, device) if device is not None else x
    except (RuntimeError, BufferError):
        # If dlpack fails (e.g. because the array is read-only for frameworks that do not
        # support it), we create a copy of the array that we own and then convert it.
        # TODO: The correct treatment of read-only arrays is currently not fully clear in the
        # Array API. Once ongoing discussions are resolved, we should update this code to remove
        # any fallbacks.
        value_namespace = array_namespace(value)
        value_copy = value_namespace.asarray(value, copy=True)
        return xp.asarray(value_copy, device=device)

