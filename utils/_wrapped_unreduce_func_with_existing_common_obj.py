
def _wrapped_unreduce_func_with_existing_common_obj(common_obj_id):
  """Unreduces a common object that has already appeared."""
  assert _common_obj_state.common_obj is not None
  return _common_obj_state.common_obj[common_obj_id]

