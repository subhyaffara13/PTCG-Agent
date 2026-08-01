
def _tile_batch_rule(batched_args, batch_dims, *, reps):
  operand, = batched_args
  bdim, = batch_dims
  new_reps = list(reps)
  new_reps.insert(bdim, 1)
  return tile(operand, reps=new_reps), bdim

