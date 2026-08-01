
def maybe_linearize_tracer(trace, primal, is_nonzero, tangent):
  if is_nonzero:
    assert not type(tangent) is Zero
    return LinearizeTracer(trace, primal, tangent)
  else:
    assert type(tangent) is Zero
    return primal

