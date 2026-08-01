
def _coo_todense_impl(data, row, col, *, spinfo):
  return jnp.zeros(spinfo.shape, data.dtype).at[row, col].add(data)

