
def _bcoo_transpose_transpose(ct, data, indices, *, permutation: Sequence[int], spinfo: SparseInfo):
  data_ct, indices_ct = ct
  assert isinstance(indices_ct, ad.Zero)
  if ad.is_undefined_primal(indices):
    raise ValueError("Cannot transpose with respect to sparse indices")
  assert data_ct.dtype == data.aval.dtype
  ct_spinfo = SparseInfo(tuple(spinfo.shape[p] for p in permutation))
  rev_permutation = list(map(int, np.argsort(permutation)))
  # TODO(jakevdp) avoid dummy indices?
  dummy_indices = jnp.zeros([1 for i in range(indices.ndim - 2)] + list(indices.shape[-2:]), dtype=int)
  data_trans, _ = _bcoo_transpose(data_ct, dummy_indices, permutation=rev_permutation, spinfo=ct_spinfo)
  return data_trans, indices_ct

