
def _validate_jax_pjrt_client_create_options(new_val):
  if new_val is not None and not isinstance(new_val, (str, dict)):
      raise ValueError('new string config value must be None or of type dict'
                       f' | str, got {new_val} of type {type(new_val)}.')

