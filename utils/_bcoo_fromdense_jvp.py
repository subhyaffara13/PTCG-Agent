
def _bcoo_fromdense_jvp(primals, tangents, *, nse, n_batch, n_dense, index_dtype):
  M, = primals
  Mdot, = tangents

  primals_out = _bcoo_fromdense(M, nse=nse, n_batch=n_batch, n_dense=n_dense, index_dtype=index_dtype)
  data, indices = primals_out

  if type(Mdot) is ad.Zero:
    data_dot = ad.p2tz(data)
  else:
    data_dot = _bcoo_extract(indices, Mdot)

  tangents_out = (data_dot, ad.p2tz(indices))

  return primals_out, tangents_out

