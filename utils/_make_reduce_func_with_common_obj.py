
def _make_reduce_func_with_common_obj(
    reduce_func: Callable[[Any], tuple[Any, Any]],
) -> Callable[[Any], tuple[Any, Any]]:
  """Wraps a reduce function to serialize a common object once."""

  @functools.wraps(reduce_func)
  def wrapped_reduce_func(obj):
    assert _common_obj_state.common_obj_index is not None
    common_obj_id = _common_obj_state.common_obj_index.get(obj)
    if common_obj_id is None:
      unreduced_func, unreduced_args = reduce_func(obj)
      common_obj_id = len(_common_obj_state.common_obj_index)
      _common_obj_state.common_obj_index[obj] = common_obj_id
      return _wrapped_unreduce_func_with_new_common_obj, (
          common_obj_id, unreduced_func, unreduced_args)
    else:
      return _wrapped_unreduce_func_with_existing_common_obj, (common_obj_id,)

  return wrapped_reduce_func

