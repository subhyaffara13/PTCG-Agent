
def _make_flat_callback(in_tree, callback, static_args):
  def _flat_callback(*dyn_args):
    args, kwargs = merge_callback_args(in_tree, dyn_args, static_args)
    callback(*args, **kwargs)
    return ()
  return _flat_callback

