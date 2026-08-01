
def _csr_fromdense_jvp(primals, tangents, *, nse, index_dtype):
  M, = primals
  Mdot, = tangents

  primals_out = _csr_fromdense(M, nse=nse, index_dtype=index_dtype)
  data, indices, indptr = primals_out

  if type(Mdot) is ad.Zero:
    data_dot = ad.p2tz(data)
  else:
    data_dot = _csr_extract(indices, indptr, Mdot)

  tangents_out = (data_dot, ad.p2tz(indices), ad.p2tz(indptr))

  return primals_out, tangents_out

