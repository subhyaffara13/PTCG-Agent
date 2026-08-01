
def _ragged_dot_general_impl(
    lhs: Array,
    rhs: Array,
    group_sizes: Array,
    ragged_dot_dimension_numbers: RaggedDotDimensionNumbers,
    precision: PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    group_offset: Array | None = None,
    out_sharding: NamedSharding | P | None = None,
    ) -> Array:
  if group_offset is not None:
    raise NotImplementedError("Unimplemented group_offset support.")

  def ragged_to_dense(x: Array, gs: Array, *, dim: int):
    from jax._src.lax import control_flow  # avoid circular imports
    assert gs.ndim == 1
    shape = gs.shape + x.shape
    x = broadcast_in_dim(x, shape, list(range(1, len(shape))))
    iota = broadcasted_iota(gs.dtype, shape, dim+1)
    group_ends = control_flow.cumsum(gs)
    group_starts = concatenate(
        [_zeros(gs)[:1], group_ends[:-1]],
        dimension=0,
    )
    group_ends = broadcast_in_dim(group_ends, shape, (0,))
    group_starts = broadcast_in_dim(group_starts, shape, (0,))
    mask = bitwise_and(group_starts <= iota, iota < group_ends)
    x = select(mask, x, _zeros(x))
    return x

  def batched_ragged_to_dense(dim, *x_in_axes: int):
    if not x_in_axes:
      return partial(ragged_to_dense, dim=dim)
    x_axis, *rest = x_in_axes
    decr = lambda d: d - 1 if d >= x_axis else d
    return api.vmap(
        batched_ragged_to_dense(decr(dim), *[decr(ax) for ax in rest]),
        in_axes=(x_axis, 0),
    )

  incr = lambda dims: [d + 1 for d in dims]

  # Expand the ragged `dim` of `x`, given its batching `axes`.
  # The group axis from `gs` becomes the outermost axis of the result.
  # Some examples:
  #   x: [m,k]      , gs: [g]       ==> expand(x, 0, gs): [g,m,k]
  #   x: [b1,m,b2,k], gs: [b1,b2,g] ==> expand(x, 1, gs, 0, 2): [g,b1,m,b2,k]
  def expand(x, dim, gs, *axes):
    expanded = batched_ragged_to_dense(dim, *axes)(x, gs)
    unsorted_dims = incr(axes) + [0] + incr(remaining(range(x.ndim), axes))
    return transpose(expanded, np.argsort(unsorted_dims))

  mode, lhs_ragged_dim = _ragged_dot_mode_and_dim(
      lhs.ndim, ragged_dot_dimension_numbers
  )
  (l_contract, r_contract), (l_batch, r_batch) = (
      ragged_dot_dimension_numbers.dot_dimension_numbers
  )
  l_prefix = _ragged_dot_prefix_dims(
      mode, lhs.ndim, lhs_ragged_dim, l_batch, l_contract
  )

  _dot_general = partial(
      dot_general,
      precision=precision,
      preferred_element_type=preferred_element_type,
  )
  # TODO(pravnar): Permit other broadcastable shapes.
  if group_sizes.ndim == 1:
    group_sizes = broadcast(group_sizes, [lhs.shape[i] for i in l_prefix])

  match mode:
    case RaggedDotMode.RAGGED_NONCONTRACTING:
      rhs_group_dims = ragged_dot_dimension_numbers.rhs_group_dimensions
      assert len(rhs_group_dims) == 1
      return _dot_general(
          expand(lhs, lhs_ragged_dim, group_sizes, *l_prefix),
          rhs,
          dimension_numbers=(
              (incr(l_contract) + [0], list(r_contract) + [rhs_group_dims[0]]),
              (incr(l_batch), r_batch),
          ),
          out_sharding=out_sharding,
      )
    case RaggedDotMode.RAGGED_CONTRACTING:
      rhs_ragged_dim = r_contract[l_contract.index(lhs_ragged_dim)]
      r_prefix = _ragged_dot_prefix_dims(
        mode, rhs.ndim, rhs_ragged_dim, r_batch, r_contract
      )
      return _dot_general(
          expand(lhs, lhs_ragged_dim, group_sizes, *l_prefix),
          expand(rhs, rhs_ragged_dim, group_sizes, *r_prefix),
          dimension_numbers=(
              (incr(l_contract), incr(r_contract)),
              ([0] + incr(l_batch), [0] + incr(r_batch)),
          ),
          out_sharding=out_sharding,
      )
    case RaggedDotMode.RAGGED_BATCH:
      return _dot_general(
          lhs,
          rhs,
          dimension_numbers=ragged_dot_dimension_numbers.dot_dimension_numbers,
          out_sharding=out_sharding,
      )

