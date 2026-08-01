
def bcoo_broadcast_in_dim(mat: BCOO, *, shape: Shape, broadcast_dimensions: Sequence[int],
                          sharding=None) -> BCOO:
  """Expand the size and rank of a BCOO array by duplicating the data.

  A BCOO equivalence to jax.lax.broadcast_in_dim.

  Args:
    mat: A BCOO-format array.
    shape: The shape of the target array.
    broadcast_dimensions: The dimension in the shape of the target array which
      each dimension of the operand (``mat``) shape corresponds to.

  Returns:
    A BCOO-format array containing the target array.
  """
  return BCOO(_bcoo_broadcast_in_dim(mat.data, mat.indices, spinfo=mat._info,
                                     shape=shape,
                                     broadcast_dimensions=broadcast_dimensions),
              shape=shape)

