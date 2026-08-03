import math


def _build_axis_index_lowering_hlo(ctx, axis_name, axis_ctx):
  from jax._src.shard_map import shard_map  # pyrefly: ignore[missing-import]

  if isinstance(axis_name, tuple):
    assert axis_name, 'empty axis name'
    if len(axis_name) > 1:
      raise NotImplementedError(
          '`axis_index` lowering rule does not support multiple axis names.')
    axis_name, = axis_name

  if isinstance(axis_ctx, SPMDAxisContext):
    size = axis_ctx.mesh.size
    axis_names = axis_ctx.mesh.axis_names
    axis_sizes = axis_ctx.mesh.axis_sizes
  else:
    assert isinstance(axis_ctx, ShardingContext)
    size, axis_names, axis_sizes = 1, (), ()

  if axis_name not in axis_names:
    raise NameError(f"unbound axis name: {axis_name}")
  axis_pos = list(axis_names).index(axis_name)

  # For partial auto, enter into a fully manual shard_map.
  if (isinstance(axis_ctx, SPMDAxisContext) and
      axis_ctx.manual_axes and
      axis_ctx.manual_axes != frozenset(axis_ctx.mesh.axis_names)):
    if axis_sizes[axis_pos] == 1:
      return hlo.constant(ir.DenseElementsAttr.get(np.asarray(0, dtype=np.int32)))
    def f():
      return axis_index_p.bind(axis_name=axis_name)
    return mlir.lower_fun(lambda: [shard_map(f, check_vma=False, in_specs=(),
                                             out_specs=P())()]
                          )(ctx)[0]

  nreplicas = size // math.prod(axis_sizes)
  div = mlir.ir_constant(
      np.array(
          nreplicas * math.prod(axis_sizes[axis_pos + 1 :]), dtype=np.uint32
      )
  )
  mod = mlir.ir_constant(np.array(axis_sizes[axis_pos], dtype=np.uint32))
  if isinstance(axis_ctx, (ShardingContext, SPMDAxisContext)):
    device_id = hlo.partition_id()
  else:
    device_id = hlo.replica_id()
  unsigned_index = hlo.remainder(hlo.divide(device_id, div), mod)
  return hlo.convert(
      ir.RankedTensorType.get([], ir.IntegerType.get_signless(32)),
      unsigned_index)

