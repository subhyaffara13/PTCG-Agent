
def debug_print_impl(
    *args: Any,
    fmt: str,
    ordered,
    partitioned,
    in_tree,
    static_args,
    np_printoptions,
    has_placeholders,
    logging_record,
):
  callback = partial(
      _format_print_callback, fmt, dict(np_printoptions), has_placeholders,
      logging_record,
  )
  callback = _make_flat_callback(in_tree, callback, static_args)
  effect = ordered_debug_effect if ordered else debug_effect
  debug_callback_impl(
      *args, callback=callback, effect=effect, partitioned=partitioned
  )
  return ()

