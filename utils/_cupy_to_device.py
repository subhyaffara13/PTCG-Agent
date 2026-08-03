from typing import Any

def _cupy_to_device(
    x: cp.ndarray,
    device: Device,
    /,
    stream: int | Any | None = None,
) -> cp.ndarray:
    import cupy as cp

    if device == "cpu":
        # allowing us to use `to_device(x, "cpu")`
        # is useful for portable test swapping between
        # host and device backends
        return x.get()
    if not isinstance(device, cp.cuda.Device):
        raise TypeError(f"Unsupported device type {device!r}")

    if stream is None:
        with device:
            return cp.asarray(x)

    # stream can be an int as specified in __dlpack__, or a CuPy stream
    if isinstance(stream, int):
        stream = cp.cuda.ExternalStream(stream)
    elif not isinstance(stream, cp.cuda.Stream):
        raise TypeError(f"Unsupported stream type {stream!r}")

    with device, stream:
        return cp.asarray(x)

