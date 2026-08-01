
def _debug_callback_partial_auto(axis_context, *args, **params):
  partial_auto = list(set(axis_context.mesh.axis_names) - axis_context.manual_axes)
  def f():
    idx = lax.axis_index(*partial_auto)
    return lax.cond(idx == 0,
                    lambda: debug_callback_p.bind(*args, **params),
                    lambda: [])
  return shard_map.shard_map(f, in_specs=(), out_specs=[])()

