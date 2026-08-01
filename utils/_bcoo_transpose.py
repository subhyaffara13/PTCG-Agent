
def _bcoo_transpose(data: Array, indices: Array, *,
                    permutation: Sequence[int], spinfo: SparseInfo) -> tuple[Array, Array]:
  permutation = tuple(permutation)
  if permutation == tuple(range(len(spinfo.shape))):
    return data, indices
  else:
    return bcoo_transpose_p.bind(data, indices, permutation=permutation,
                                 spinfo=spinfo)

