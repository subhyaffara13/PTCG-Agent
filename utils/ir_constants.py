from typing import Any

def ir_constants(
    val: Any, *,
    const_lowering: dict[tuple[int, core.AbstractValue], IrValues] | None = None,
    aval: core.AbstractValue | None = None
) -> tuple[ir.Value, ...]:
  """Translate a Python ``val`` to a sequence of IR constants.

  See https://docs.jax.dev/en/latest/internals/constants.html.

  Args:
    val: a Python value to be translated.
    const_lowering: an optional dictionary with known lowering for some
      constants, indexed by ``id``. This is used, e.g., when we pass constants
      as MLIR function arguments.
    aval: the abstract value of ``val``, if known. Required where ambiguous,
      e.g. for Python scalars.

  Returns:
    A representation of the constant as a sequence of IR values.

  Raises:
    TypeError: if no constant handler is registered for the type of ``val``.
  """
  values = _ir_constant(val, const_lowering=const_lowering, aval=aval)
  return values if isinstance(values, tuple) else (values,)

