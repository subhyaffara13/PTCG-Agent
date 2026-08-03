from typing import Any

def ir_constant(
    val: Any, *,
    const_lowering: dict[tuple[int, core.AbstractValue], IrValues] | None = None,
    aval: core.AbstractValue | None = None
) -> ir.Value:
  """Translate a Python ``val`` to an IR constant.

  See https://docs.jax.dev/en/latest/internals/constants.html.

  Args:
    val: a Python value to be translated to a constant.
    const_lowering: an optional dictionary with known lowering for some
      constants, indexed by ``id``. This is used, e.g., when we pass constants
      as MLIR function arguments.
    aval: the abstract value of ``val``, if known. Required where ambiguous,
      e.g. for Python scalars.

  Returns:
    A representation of the constant as an IR value.

  Raises:
    ValueError: if the constant is represented by more than one IR value.
    TypeError: if no constant handler is registered for the type of `val`.
  """
  value = _ir_constant(val, const_lowering=const_lowering, aval=aval)
  if isinstance(value, tuple):
    raise ValueError(
        f"Expected a constant to produce a single ir.Value, got {value}"
    )
  return value


def ir_constant(x: Any, mlir_type: ir.Type | None = None) -> ir.Value:
  if mlir_type is None:
    dtype = getattr(x, "dtype", None)
    if dtype is None:
      if isinstance(x, int):
        mlir_type = ir.IntegerType.get_signless(32)
      elif isinstance(x, float):
        mlir_type = ir.F32Type.get()
      else:
        raise ValueError(f"Cannot determine dtype for {x}")
    else:
      mlir_type = _dtype_to_ir_type(dtype)
  if isinstance(x, (bool, int, float)):
    return jax_mlir_ext.arith_constant(x, mlir_type)
  if jnp.issubdtype(x.dtype, np.integer):
    return jax_mlir_ext.arith_constant(int(x), mlir_type)
  elif jnp.issubdtype(x.dtype, jnp.floating):
    return jax_mlir_ext.arith_constant(float(x), mlir_type)
  elif x.dtype == jnp.bool_:
    return jax_mlir_ext.arith_constant(bool(x), mlir_type)
  raise NotImplementedError(x.dtype)

