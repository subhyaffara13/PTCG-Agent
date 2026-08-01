
def _ir_constant(val: Any, *,
  const_lowering: dict[tuple[int, core.AbstractValue], IrValues] | None = None,
  aval: core.AbstractValue | None = None
) -> IrValues:
  if const_lowering is not None:
    # pyrefly: ignore[bad-argument-type]
    if np.shape(val) and (c_val := const_lowering.get((id(val), aval))) is not None:
      return c_val
  for t in type(val).__mro__:
    handler = _constant_handlers.get(t)
    if handler:
      out = handler(val, aval)
      assert _is_ir_values(out), (type(val), out)
      return out
  m = getattr(val, '__jax_array__', None)
  if m is not None:
    return ir_constant(m())
  raise TypeError(f"No constant handler for type: {type(val)}")


def _ir_constant(v: object, t: ir.Type) -> ir.Value:
  if isinstance(
      v, (np.number, np.ndarray, int, float, jax_literals.TypedNdArray)
  ):
    if isinstance(t, (ir.IntegerType, ir.IndexType)):
      v = int(v)
    else:
      assert isinstance(t, ir.FloatType)
      v = float(v)
    return arith_dialect.constant(t, v)
  raise NotImplementedError(f"Unsupported constant: {v!r}")


def _ir_constant(v: object, t: ir.Type) -> ir.Value:
  if isinstance(
      v, (np.number, np.ndarray, int, float, literals.TypedNdArray)
  ):
    if isinstance(t, ir.IntegerType):
      v = int(v)
    else:
      assert isinstance(t, ir.FloatType)
      v = float(v)
    return arith_dialect.constant(t, v)
  raise NotImplementedError

