
def _reduce_scatter_start_lowering(ctx, x, *, tiled, **kwargs):
  if not tiled:
    # TODO(mwhittaker): When the output is not tiled, a reduce_scatter is
    # lowered to two operations: a reduce_scatter and a reshape. Lowering the
    # async version of this is tricky because we need to reshape after the
    # future is resolved.
    raise NotImplementedError("lowering reduce_scatter_start with tiled=False unimplemented")
  lower = partial(_reduce_scatter_lowering, lax.add_p)
  return _start_lowering(lower)(ctx, x, tiled=tiled, **kwargs)

