
def _invalid_shape_error(shape: Shape, context: str=""):
  msg = ("Shapes must be 1D sequences of concrete values of integer type, "
         f"got {shape}.")
  if context:
    msg += f" {context}."
  if any(isinstance(x, Tracer) and isinstance(typeof(x), ShapedArray)
         and not is_concrete(x) for x in shape):
    msg += ("\nIf using `jit`, try using `static_argnums` or applying `jit` to "
            "smaller subfunctions.")
    for x in shape:
      if isinstance(x, Tracer) and hasattr(x, "_origin_msg"):
        msg += x._origin_msg()

  return TypeError(msg)

