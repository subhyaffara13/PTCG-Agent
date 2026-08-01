
def _jvp_jaxpr_zeros(f, store, in_zeros, zero_avals, *primal_tangent_avals):
  in_primals, nz_in_tangents = split_list(primal_tangent_avals, [len(in_zeros)])
  symbolic_zeros = map(ad_util.SymbolicZero, zero_avals)
  tangents = merge_lists(in_zeros, nz_in_tangents, symbolic_zeros)
  out = f(*in_primals, *tangents)
  n, ragged = divmod(len(out), 2)
  assert not ragged
  out_primals, out_tangents = out[:n], out[n:]
  out_zeros = [type(t) is ad_util.SymbolicZero for t in out_tangents]
  out_nz_tangents, _ = partition_list(out_zeros, out_tangents)
  store.store(out_zeros)
  return [*out_primals, *out_nz_tangents]

