
def _check_aval_is_supported(caller: str, aval: jax_core.ShapedArray) -> None:
  supported_shapes = sc_core.supported_shapes(aval.dtype)
  if aval.shape in supported_shapes:
    return
  if not supported_shapes:
    raise NotImplementedError(f"{caller} does not support {aval.dtype} arrays")
  else:
    raise NotImplementedError(
        f"{caller} only supports {aval.dtype} arrays of shapes"
        f" [{', '.join(map(repr, supported_shapes))}], got {aval.shape}"
    )

