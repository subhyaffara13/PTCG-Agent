
def to_elt(trace: BatchTrace, get_idx: GetIdx, x: Vmappable, spec: MapSpec) -> Elt:
  from jax._src import hijax  # pyrefly: ignore[missing-module-attribute]
  handler = to_elt_handlers.get(type(x))
  if handler:
    return handler(partial(to_elt, trace, get_idx), get_idx, x, spec)
  elif isinstance(spec, int) or spec is None:
    spec = None if spec is None else canonicalize_axis(spec, len(np.shape(x)))
    return (BatchTracer(trace, x, spec, source_info_util.current())
            if spec is not None else x)
  elif isinstance(typeof(x), hijax.HiType):
    # TODO check possible errors
    return BatchTracer(trace, x, spec, source_info_util.current())
  else:
    assert False, f'Unexpected type in ELT? {type(x)}'

