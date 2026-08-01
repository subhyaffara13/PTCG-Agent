
def _bcoo_transpose_jvp(primals, tangents, *, permutation: Sequence[int], spinfo: SparseInfo):
  data, indices = primals
  data_dot, _ = tangents
  primals_out = _bcoo_transpose(data, indices, permutation=permutation, spinfo=spinfo)
  data_dot_out, _ = _bcoo_transpose(data_dot, indices, permutation=permutation, spinfo=spinfo)
  return primals_out, (data_dot_out, ad.p2tz(indices))

