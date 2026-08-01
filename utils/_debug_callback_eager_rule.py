
def _debug_callback_eager_rule(
    mesh,
    *args,
    callback: Callable[..., Any],
    effect: DebugEffect,
    partitioned: bool,
):
  del effect
  with core.eval_context():
    all_blocks = zip(*map(list, args))
  for (idx, device), blocks in zip(np.ndenumerate(mesh.devices), all_blocks):
    callback(*blocks)
  return []

