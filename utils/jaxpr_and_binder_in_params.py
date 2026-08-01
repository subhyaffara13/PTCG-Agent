
def jaxpr_and_binder_in_params(params, index: int) -> Iterator[tuple[core.Jaxpr, core.Var]]:
  for val in params.values():
    vals = val if isinstance(val, tuple) else (val,)
    for v in vals:
      if isinstance(v, core.Jaxpr):
        if index >= len(v.invars):
          raise RuntimeError(f"Failed to find index {index} in jaxpr.invars while building report")
        yield v, v.invars[index]
      elif isinstance(v, core.ClosedJaxpr):
        if index >= len(v.jaxpr.invars):
          raise RuntimeError(f"Failed to find index {index} in jaxpr.invars while building report")
        yield v.jaxpr, v.jaxpr.invars[index]

