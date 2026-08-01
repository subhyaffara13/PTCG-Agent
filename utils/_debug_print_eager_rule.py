
def _debug_print_eager_rule(
    mesh,
    *args,
    fmt: str,
    ordered,
    partitioned,
    in_tree,
    static_args,
    np_printoptions,
    has_placeholders,
    logging_record,
):
  del ordered, partitioned
  callback = partial(
      _format_print_callback, fmt, dict(np_printoptions), has_placeholders,
      logging_record,
  )
  callback = _make_flat_callback(in_tree, callback, static_args)
  with core.eval_context():
    all_blocks = zip(*map(list, args))
  for (idx, device), blocks in zip(np.ndenumerate(mesh.devices), all_blocks):
    callback(*blocks)
  return []

