
def bcsr_broadcast_in_dim(mat: BCSR, *, shape: Shape, broadcast_dimensions: Sequence[int],
                          sharding=None) -> BCSR:
  result_bcoo = bcoo.bcoo_broadcast_in_dim(
    mat.to_bcoo(), shape=shape, broadcast_dimensions=broadcast_dimensions)
  return BCSR.from_bcoo(result_bcoo)

