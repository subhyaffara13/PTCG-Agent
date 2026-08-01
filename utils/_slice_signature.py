
def _slice_signature(eqn):
  in_aval = eqn.invars[0].aval
  assert hasattr(in_aval, "dtype")
  if not jax.dtypes.issubdtype(in_aval.dtype, jax.dtypes.prng_key):
    return KeyReuseSignature(Forward(0, 0))
  assert hasattr(in_aval, "shape")
  if any(core.is_symbolic_dim(s) for s in in_aval.shape):
    return KeyReuseSignature(Forward(0, 0))
  start_indices = eqn.params['start_indices']
  limit_indices = eqn.params['limit_indices']
  strides = eqn.params['strides'] or (1,) * len(start_indices)
  idx = tuple(slice(*tup) for tup in util.safe_zip(start_indices, limit_indices, strides))
  sink = np.zeros(in_aval.shape, dtype=bool)
  sink[idx] = True
  return KeyReuseSignature(Sink(0, sink), Source(0))

