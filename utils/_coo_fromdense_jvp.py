
def _coo_fromdense_jvp(primals, tangents, *, nse, index_dtype):
  M, = primals
  Mdot, = tangents

  primals_out = _coo_fromdense(M, nse=nse, index_dtype=index_dtype)
  data, row, col = primals_out

  if type(Mdot) is ad.Zero:
    data_dot = ad.p2tz(data)
  else:
    data_dot = _coo_extract(row, col, Mdot)

  tangents_out = (data_dot, ad.p2tz(row), ad.p2tz(col))

  return primals_out, tangents_out

