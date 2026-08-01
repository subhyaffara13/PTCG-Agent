
def _tile_abstract_eval(x, reps):
  if x.ndim != len(reps):
    raise TypeError(
        f"reps length must be equal to the ndim of x, got {len(reps)=} "
        f"and {x.ndim=}.")
  for i, (r, sh) in enumerate(zip(reps, x.sharding.spec)):
    if r != 1 and sh is not None:
      raise core.ShardingTypeError(
          f'Operand cannot be sharded on dimension {i} when the tiling is'
          f' non-trivial. Got input type: {x} with reps: {reps}')
  return x.update(shape=tuple(np.multiply(x.shape, reps)))

