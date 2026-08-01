
def assert_func(error: Error, pred: Bool, new_error: JaxException) -> Error:
  code = next_code()
  effect_type = new_error.get_effect_type()
  new_payload, new_metadata = tree_flatten(new_error)
  return update_error(error, pred, code, {code: new_metadata}, new_payload, effect_type)

