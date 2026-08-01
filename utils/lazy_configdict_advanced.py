
def lazy_configdict_advanced():
  """Advanced lazy computation with ConfigDict."""
  # FieldReferences can be used with ConfigDict as well
  config = config_dict.ConfigDict()
  config.float_field = 12.6
  config.integer_field = 123
  config.list_field = [0, 1, 2]

  config.float_multiply_field = config.get_ref('float_field') * 3
  print(config.float_multiply_field)  # Prints 37.8

  config.float_field = 10.0
  print(config.float_multiply_field)  # Prints 30.0

  config.longer_list_field = config.get_ref('list_field') + [3, 4, 5]
  print(config.longer_list_field)  # Prints [0, 1, 2, 3, 4, 5]

  config.list_field = [-1]
  print(config.longer_list_field)  # Prints [-1, 3, 4, 5]

  # Both operands can be references
  config.ref_subtraction = (
      config.get_ref('float_field') - config.get_ref('integer_field'))
  print(config.ref_subtraction)  # Prints -113.0

  config.integer_field = 10
  print(config.ref_subtraction)  # Prints 0.0

