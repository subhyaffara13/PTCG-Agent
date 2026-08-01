
def _auto_submodule_name(parent_ctx, cls):
  """Increment type count and generate a new submodule name."""
  type_index = parent_ctx.type_counter[cls]
  parent_ctx.type_counter[cls] += 1
  return f'{cls.__name__}_{type_index}'

