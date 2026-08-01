
def required_placeholder(field_type):
  """Defines an entry in a ConfigDict with unknown but required value.

  Example::

    config = configdict.create(
        batch_size = configdict.required_placeholder(int))

    try:
      print(config.batch_size)
    except RequiredValueError:
      pass

    config.batch_size = 10
    print(config.batch_size)  # 10

  Args:
    field_type: type of value.

  Returns:
    A `FieldReference` with value None and the given type.
  """
  return placeholder(field_type, required=True)

