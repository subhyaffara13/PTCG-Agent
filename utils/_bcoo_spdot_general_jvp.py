
def _bcoo_spdot_general_jvp(primals, tangents, **kwds):
  lhs_data, lhs_indices, rhs_data, rhs_indices = primals
  lhs_data_dot, lhs_indices_dot, rhs_data_dot, rhs_indices_dot = tangents
  primals_out = _bcoo_spdot_general(*primals, **kwds)
  assert type(lhs_indices_dot) is ad.Zero
  assert type(rhs_indices_dot) is ad.Zero
  data_dot_out = 0
  if type(lhs_data_dot) is not ad.Zero:
    data_dot_out += _bcoo_spdot_general(lhs_data_dot, lhs_indices, rhs_data, rhs_indices, **kwds)[0]
  if type(rhs_data_dot) is not ad.Zero:
    data_dot_out += _bcoo_spdot_general(lhs_data, lhs_indices, rhs_data_dot, rhs_indices, **kwds)[0]
  return primals_out, [data_dot_out, ad.p2tz(primals_out[1])]

