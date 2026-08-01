
def _is_materializable(x: Array) -> bool:
    """
    Return True if you can call `as_numpy_array(x)`; False otherwise.
    """
    # Important: here we assume that we're not tracing -
    # e.g. we're not inside `jax.jit`` nor `cupy.cuda.Stream.begin_capture`.
    return not is_torch_array(x) or x.device.type != "meta"  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]

