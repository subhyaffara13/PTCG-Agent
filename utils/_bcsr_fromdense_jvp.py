
def _bcsr_fromdense_jvp(primals, tangents, *, nse, n_batch, n_dense, index_dtype):
  M, = primals
  Mdot, = tangents

  primals_out = _bcsr_fromdense(M, nse=nse, n_batch=n_batch, n_dense=n_dense, index_dtype=index_dtype)
  data, indices, indptr = primals_out

  if type(Mdot) is ad.Zero:
    data_dot = ad.p2tz(data)
  else:
    data_dot = bcsr_extract(indices, indptr, Mdot)

  tangents_out = (data_dot, ad.p2tz(indices), ad.p2tz(indptr))

  return primals_out, tangents_out

