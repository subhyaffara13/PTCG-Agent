
def trace_value(value: _ods_ir.Value, label: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TraceValueOp:
  return TraceValueOp(value=value, label=label, loc=loc, ip=ip)


def trace_value(label: str, value: jax.Array) -> None:
  """Emit a scalar value to the current xprof trace scope.

  This appends a dynamic scalar value to the enclosing trace region.
  The value will appear in xprof trace viewer associated with the trace event.

  Args:
    label: A string label for this value in xprof.
    value: A scalar i32 or f32 value to emit.

  Example:
    # Inside a Pallas kernel:
    x  = jnp.sum(y > 0)
    pltpu.trace_value("my_x", x)
  """
  trace_value_p.bind(value, label=label)

