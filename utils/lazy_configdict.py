
def lazy_configdict():
  """Example usage of lazy computation with ConfigDict."""
  config = config_dict.ConfigDict()
  config.reference_field = config_dict.FieldReference(1)
  config.integer_field = 2
  config.float_field = 2.5

  # No lazy evaluatuations because we didn't use get_ref()
  config.no_lazy = config.integer_field * config.float_field

  # This will lazily evaluate ONLY config.integer_field
  config.lazy_integer = config.get_ref('integer_field') * config.float_field

  # This will lazily evaluate ONLY config.float_field
  config.lazy_float = config.integer_field * config.get_ref('float_field')

  # This will lazily evaluate BOTH config.integer_field and config.float_Field
  config.lazy_both = (config.get_ref('integer_field') *
                      config.get_ref('float_field'))

  config.integer_field = 3
  print(config.no_lazy)  # Prints 5.0 - It uses integer_field's original value

  print(config.lazy_integer)  # Prints 7.5

  config.float_field = 3.5
  print(config.lazy_float)  # Prints 7.0
  print(config.lazy_both)  # Prints 10.5

