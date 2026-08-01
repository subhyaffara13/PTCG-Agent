
def jaxprs_in_params(params) -> Iterator[Jaxpr]:
  for val in params.values():
    vals = val if isinstance(val, tuple) else (val,)
    for v in vals:
      if isinstance(v, Jaxpr):
        yield v
      elif isinstance(v, ClosedJaxpr):
        yield v.jaxpr

