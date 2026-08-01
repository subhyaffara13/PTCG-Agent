
def _wrapped_unreduce_func_with_new_common_obj(
    common_obj_id, unreduce_func, unreduce_args):
  """Unreduces a new common object."""
  assert _common_obj_state.common_obj is not None
  obj = unreduce_func(*unreduce_args)
  assert len(_common_obj_state.common_obj) == common_obj_id, (
      f"Expected {common_obj_id} common objects, but got"
      f" {len(_common_obj_state.common_obj)}. This can happen if serialization"
      " and deserialization of objects happened in different orders."
  )
  _common_obj_state.common_obj.append(obj)
  return obj

