
def _on_batch_callback(
    infos: Sequence[types.ParamInfo],
    callback_fn: Callable[..., None],
) -> None:
  """Launches callback for each info."""
  for info in infos:
    callback_fn(info.keypath)

