
def _unreduced_reduce_scatter_start_lowering(ctx, x, *, tiled, **kwargs):
  if not tiled:
    msg = (
        "lowering unreduced_reduce_scatter_start with tiled=False unimplemented"
    )
    raise NotImplementedError(msg)
  lower = partial(_unreduced_reduce_scatter_lowering, lax.add_p)
  return _start_lowering(lower)(ctx, x, tiled=tiled, **kwargs)

