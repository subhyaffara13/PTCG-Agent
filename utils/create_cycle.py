
def create_cycle():
  """Creates a cycle within a ConfigDict."""
  config = config_dict.ConfigDict()
  config.integer_field = 1
  config.bigger_integer_field = config.get_ref('integer_field') + 10

  try:
    # Raises a MutabilityError because setting config.integer_field would
    # cause a cycle.
    config.integer_field = config.get_ref('bigger_integer_field') + 2
  except config_dict.MutabilityError as e:
    print(e)

