
def _token_global_result_handler(global_aval, out_sharding, committed):
  array_handler = _array_global_result_handler(
      core.get_token_aval(), out_sharding, committed)
  def wrapper(array):
    return core.Token(array)
  return array_handler.wrap(wrapper)

